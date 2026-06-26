param(
    [string]$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $Repo

$sourceDocs = @(
    "AGENTS.md",
    "CLAUDE.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "MISSION-STATEMENT.md",
    "README.md",
    "SECURITY.md"
)
$allEmojiDocs = $sourceDocs + @("EMOJI.md")

foreach ($doc in $allEmojiDocs) {
    $path = Join-Path "emoji" $doc
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing $path"
    }
}

foreach ($doc in $sourceDocs) {
    $diff = git diff -- $doc
    if ($diff) {
        throw "Original documentation changed unexpectedly: $doc"
    }
}

if (-not (Test-Path -LiteralPath "EMOJI.md")) {
    throw "Missing root EMOJI.md"
}

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("agentpipe-emoji-check-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
try {
    foreach ($doc in $sourceDocs) {
        $generated = Join-Path $tmp $doc
        & (Join-Path $PSScriptRoot "Convert-EmojiDocs.ps1") -Direction AsciiToEmoji -InputPath (Join-Path $Repo $doc) -OutputPath $generated
        $expected = Get-Content -LiteralPath $generated -Raw
        $actual = Get-Content -LiteralPath (Join-Path $Repo "emoji\$doc") -Raw
        if ($expected -ne $actual) {
            throw "Emoji translation drift for $doc"
        }

        $decoded = Join-Path $tmp ($doc + ".decoded.txt")
        & (Join-Path $PSScriptRoot "Convert-EmojiDocs.ps1") -Direction EmojiToAscii -InputPath (Join-Path $Repo "emoji\$doc") -OutputPath $decoded
        if ((Get-Content -LiteralPath $decoded -Raw) -match "\[unknown:") {
            throw "Reverse translation has unknown tokens for $doc"
        }
    }

    $source = Get-Content -LiteralPath "EMOJI.md" -Raw
    $translatedGuide = Join-Path $tmp "EMOJI.md"
    & (Join-Path $PSScriptRoot "Convert-EmojiDocs.ps1") -Direction AsciiToEmoji -InputPath (Join-Path $Repo "EMOJI.md") -OutputPath $translatedGuide
    $guideExpected = Get-Content -LiteralPath $translatedGuide -Raw
    $guideActual = Get-Content -LiteralPath "emoji\EMOJI.md" -Raw
    if ($guideExpected -ne $guideActual) {
        throw "Emoji translation drift for emoji/EMOJI.md"
    }
} finally {
    Remove-Item -LiteralPath $tmp -Recurse -Force
}

foreach ($doc in $sourceDocs) {
    $source = Get-Content -LiteralPath $doc
    $translated = Get-Content -LiteralPath (Join-Path "emoji" $doc)

    $sourceHeadings = ($source | Where-Object { $_ -match "^#" }).Count
    $translatedHeadings = ($translated | Where-Object { $_ -match "^#" }).Count
    $sourceLists = ($source | Where-Object { $_ -match "^\s*([-*+] |\d+\. )" }).Count
    $translatedLists = ($translated | Where-Object { $_ -match "^\s*([-*+] |\d+\. )" }).Count
    $sourceFences = ($source | Where-Object { $_ -match '^\s*```' }).Count
    $translatedFences = ($translated | Where-Object { $_ -match '^\s*```' }).Count

    if ($sourceHeadings -ne $translatedHeadings) {
        throw "Heading count mismatch for ${doc}: $sourceHeadings/$translatedHeadings"
    }
    if ($sourceLists -ne $translatedLists) {
        throw "List count mismatch for ${doc}: $sourceLists/$translatedLists"
    }
    if ($sourceFences -ne $translatedFences) {
        throw "Code fence count mismatch for ${doc}: $sourceFences/$translatedFences"
    }
}

$emojiGuide = Get-Content -LiteralPath "emoji\EMOJI.md"
$emojiGuideTableRows = ($emojiGuide | Where-Object { $_ -match "^\s*\|" }).Count
if ($emojiGuideTableRows -lt 10) {
    throw "emoji/EMOJI.md table structure was not preserved"
}

$emojiFiles = @("EMOJI.md") + (Get-ChildItem -LiteralPath "emoji" -File | ForEach-Object { $_.FullName })
$emojiText = ($emojiFiles | ForEach-Object { Get-Content -LiteralPath $_ -Raw }) -join "`n"
if ($emojiText -match "[A-Za-z]") {
    throw "ASCII letters remain in emoji documentation"
}
$alphabetPlaceholder = [char]::ConvertFromUtf32(0x1F524)
$puzzlePlaceholder = [char]::ConvertFromUtf32(0x1F9E9)
$banana = [char]::ConvertFromUtf32(0x1F34C)
$placeholderPattern = [regex]::Escape($alphabetPlaceholder) + "|" + [regex]::Escape($puzzlePlaceholder)
if ($emojiText -match $placeholderPattern) {
    throw "Placeholder emoji remain in emoji documentation"
}
if ($emojiText -match "[\uD83C][\uDDE6-\uDDFF]") {
    throw "Regional indicator flag fallback remains in emoji documentation"
}

$bananaCount = ([regex]::Matches($emojiText, [regex]::Escape($banana))).Count
$nonBananaEmojiTokenCount = ([regex]::Matches($emojiText, "[^\s|#`\-\[\]\(\)*]+")).Count - $bananaCount
if ($bananaCount -lt $nonBananaEmojiTokenCount) {
    throw "Banana ratio below 50%: bananas=$bananaCount nonBananaTokens=$nonBananaEmojiTokenCount"
}

"PASS: emoji docs match translator output, reverse translation has no unknown tokens, Markdown shape is preserved, no ASCII/placeholders/flags remain, and bananas are at least 50% of emoji tokens."

