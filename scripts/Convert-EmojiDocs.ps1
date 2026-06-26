param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("AsciiToEmoji", "EmojiToAscii")]
    [string]$Direction,

    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = "Stop"

$wordMap = @{
    "100x"="💯"; "able"="✅"; "access"="🚪"; "activities"="🎯"; "activity"="🎯"; "add"="➕"; "after"="➡️"; "aim"="🎯"; "align"="📐"; "all"="🌐"; "also"="➕"; "ambiguous"="❓"; "and"="➕"; "any"="🌐"; "apache"="📜"; "api"="🔌"; "architecture"="🏗️"; "are"="✅"; "as"="↔️"; "ask"="❓"; "at"="📍"; "atmosphere"="🌤️"; "audience"="👥"; "available"="📦"; "avoiding"="🚫"; "backend"="🖥️"; "backends"="🖥️"; "badge"="🏷️"; "banana"="🍌"; "bananas"="🍌"; "battle"="⚔️"; "because"="➡️"; "before"="⬅️"; "behavior"="🧭"; "being"="🧍"; "believe"="🤝"; "beyond"="🚀"; "bottlenecks"="🚧"; "bugs"="🐞"; "build"="🏗️"; "by"="➡️"; "call"="📞"; "can"="✅"; "capabilities"="💪"; "centered"="🎯"; "chain"="🔗"; "cheating"="🚫"; "choose"="☑️"; "clear"="🔎"; "claude"="🤖"; "code"="💻"; "coder"="👩‍💻"; "combined"="➕"; "communities"="👥"; "community"="👥"; "competition"="🏁"; "complex"="🪢"; "conduct"="🧭"; "confidential"="🔒"; "confidentiality"="🔒"; "consider"="🤔"; "contributing"="🤝"; "contribution"="🤝"; "contributions"="🤝"; "core"="🧠"; "create"="➕"; "creativity"="🎨"; "data"="🗄️"; "database"="🗄️"; "dataset"="🗃️"; "deep"="🕳️"; "dependencies"="📦"; "design"="🎨"; "deviate"="↪️"; "developer"="👩‍💻"; "different"="🔀"; "directory"="📁"; "discrimination"="🚫"; "discuss"="💬"; "distributed"="🌐"; "documentation"="📚"; "driven"="⚙️"; "engine"="🚂"; "enhancement"="✨"; "enhancements"="✨"; "environment"="🌱"; "ethical"="⚖️"; "everyone"="👥"; "exact"="🎯"; "example"="🧪"; "expected"="👀"; "experience"="🧭"; "explain"="💬"; "express"="🗣️"; "fairly"="⚖️"; "fairness"="⚖️"; "fast"="⚡"; "faster"="⚡"; "feel"="❤️"; "files"="📄"; "first"="🥇"; "fix"="🔧"; "following"="⬇️"; "for"="🎯"; "format"="🧾"; "from"="⬅️"; "fundamental"="🧠"; "gpu"="🖥️"; "granularity"="🔬"; "guidelines"="🧭"; "handle"="🤲"; "harassment"="🚫"; "hashing"="🔐"; "healthy"="💚"; "help"="🆘"; "high"="⬆️"; "hybrid"="🔀"; "if"="❓"; "impact"="💥"; "important"="⭐"; "improve"="🔧"; "in"="📍"; "including"="➕"; "indexing"="🗂️"; "information"="ℹ️"; "install"="📦"; "instructions"="🧭"; "issue"="🎫"; "issues"="🎫"; "join"="🤝"; "keep"="🔒"; "language"="🗣️"; "large"="⬆️"; "legal"="⚖️"; "license"="📜"; "lines"="📏"; "local"="📍"; "maintain"="🛠️"; "maintainers"="🛠️"; "make"="🏗️"; "may"="✅"; "memory"="🧠"; "microsecond"="⏱️"; "millions"="🔢"; "mit"="📜"; "model"="🧱"; "moral"="⚖️"; "more"="➕"; "must"="✅"; "need"="📌"; "new"="🆕"; "no"="🚫"; "node"="🟩"; "npm"="📦"; "of"="🔗"; "on"="🔛"; "online"="🌐"; "open"="📂"; "optimization"="⚙️"; "or"="↔️"; "others"="👥"; "our"="👥"; "parallelized"="🧵"; "performance"="⚡"; "permission"="✅"; "please"="🙏"; "policy"="📜"; "positive"="➕"; "pr"="🔀"; "prerequisites"="📋"; "privacy"="🔒"; "project"="📦"; "python"="🐍"; "query"="🔎"; "question"="❓"; "read"="📖"; "readme"="📘"; "real"="⏱️"; "reason"="💡"; "reasons"="💡"; "recommend"="👍"; "repository"="📦"; "report"="📝"; "reprisal"="↩️"; "requirements"="📋"; "respect"="🤝"; "respected"="🤝"; "retaliation"="↩️"; "robust"="💪"; "rules"="📏"; "run"="▶️"; "safe"="🛡️"; "security"="🔐"; "semantic"="🧠"; "set"="📦"; "simple"="▫️"; "solve"="✅"; "source"="🌱"; "speed"="⚡"; "star"="⭐"; "storage"="🗄️"; "structured"="🧱"; "suggestion"="💡"; "support"="🆘"; "system"="🖥️"; "task"="📌"; "team"="👥"; "techniques"="🛠️"; "tension"="⚖️"; "test"="🧪"; "the"="👉"; "this"="👉"; "throughput"="🚄"; "to"="➡️"; "token"="🪙"; "tokens"="🪙"; "traditional"="🏛️"; "transactions"="💸"; "treat"="🤝"; "up"="⬆️"; "use"="🛠️"; "users"="👥"; "using"="🛠️"; "values"="💎"; "vectorized"="📐"; "velocity"="⚡"; "version"="🏷️"; "vulnerability"="🔓"; "we"="👥"; "where"="📍"; "while"="⏳"; "who"="👤"; "with"="➕"; "within"="📍"; "work"="🔨"; "would"="🔮"; "you"="👉"; "your"="👉"
}

$charMap = @{
    "a"="🍎"; "b"="📘"; "c"="🍪"; "d"="🥁"; "e"="🥚"; "f"="🔥"; "g"="💎"; "h"="🏠"; "i"="ℹ️"; "j"="🕹️"; "k"="🔑"; "l"="💡"; "m"="Ⓜ️"; "n"="🧭"; "o"="⭕"; "p"="🅿️"; "q"="❓"; "r"="🌈"; "s"="⭐"; "t"="🌳"; "u"="☂️"; "v"="✅"; "w"="🌊"; "x"="❌"; "y"="🟡"; "z"="⚡";
    "0"="0️⃣"; "1"="1️⃣"; "2"="2️⃣"; "3"="3️⃣"; "4"="4️⃣"; "5"="5️⃣"; "6"="6️⃣"; "7"="7️⃣"; "8"="8️⃣"; "9"="9️⃣"
}

$reverseCharMap = @{}
foreach ($key in $charMap.Keys) {
    $reverseCharMap[$charMap[$key]] = $key
}

$reverseWordMap = @{}
foreach ($key in $wordMap.Keys) {
    if (-not $reverseWordMap.ContainsKey($wordMap[$key])) {
        $reverseWordMap[$wordMap[$key]] = $key
    }
}

function Convert-UnknownTokenToEmoji {
    param([string]$Word)
    $out = New-Object System.Collections.Generic.List[string]
    foreach ($char in $Word.ToCharArray()) {
        $key = $char.ToString().ToLowerInvariant()
        if ($charMap.ContainsKey($key)) {
            $out.Add($charMap[$key])
        }
    }
    if ($out.Count -eq 0) {
        return "❓"
    }
    return ($out -join "")
}

function Convert-WordsToEmoji {
    param([string]$Text)
    $tokens = [regex]::Matches($Text.ToLowerInvariant(), "[a-z0-9]+")
    $out = New-Object System.Collections.Generic.List[string]
    foreach ($token in $tokens) {
        $word = $token.Value
        if ($wordMap.ContainsKey($word)) {
            $out.Add($wordMap[$word])
        } else {
            $out.Add((Convert-UnknownTokenToEmoji $word))
        }
        $out.Add("🍌")
        $out.Add("🍌")
    }
    if ($out.Count -eq 0) {
        return "🍌"
    }
    return ($out -join " ")
}

function Add-BananaSeparators {
    param([string]$Text)
    $parts = [regex]::Matches($Text, "\S+")
    $out = New-Object System.Collections.Generic.List[string]
    foreach ($part in $parts) {
        if ($part.Value -eq "🍌") {
            continue
        }
        $out.Add($part.Value)
        if ($part.Value -notmatch '^[#|`\-\[\]\(\)*]+$') {
            $out.Add("🍌")
            $out.Add("🍌")
        }
    }
    if ($out.Count -eq 0) {
        return $Text
    }
    return ($out -join " ")
}

function Convert-InlineMarkdown {
    param([string]$Text)
    $converted = [regex]::Replace($Text, "!\[([^\]]*)\]\(([^)]+)\)", {
        param($m)
        "![" + (Convert-WordsToEmoji $m.Groups[1].Value) + "](" + $m.Groups[2].Value + ")"
    })
    $converted = [regex]::Replace($converted, "\[([^\]]+)\]\(([^)]+)\)", {
        param($m)
        "[" + (Convert-WordsToEmoji $m.Groups[1].Value) + "](" + $m.Groups[2].Value + ")"
    })
    $converted = [regex]::Replace($converted, "\*\*([^*]+)\*\*", {
        param($m)
        "**" + (Convert-WordsToEmoji $m.Groups[1].Value) + "**"
    })
    if ($converted -match "[A-Za-z]") {
        return Convert-WordsToEmoji $converted
    }
    return Add-BananaSeparators $converted
}

function Convert-LineToEmoji {
    param([string]$Line, [ref]$InFence)
    if ($Line -match '^\s*```') {
        $InFence.Value = -not $InFence.Value
        return '```'
    }
    if ([string]::IsNullOrWhiteSpace($Line)) {
        return $Line
    }
    if ($InFence.Value) {
        return Convert-WordsToEmoji $Line
    }
    if ($Line -match '^(#{1,6})(\s+)(.*)$') {
        return $Matches[1] + $Matches[2] + (Convert-InlineMarkdown $Matches[3])
    }
    if ($Line -match '^(\s*[-*+]\s+)(.*)$') {
        return $Matches[1] + (Convert-InlineMarkdown $Matches[2])
    }
    if ($Line -match '^(\s*\d+\.\s+)(.*)$') {
        return $Matches[1] + (Convert-InlineMarkdown $Matches[2])
    }
    if ($Line -match '^(\s*>\s?)(.*)$') {
        return $Matches[1] + (Convert-InlineMarkdown $Matches[2])
    }
    if ($Line -match '^\s*\|') {
        if ($Line -match '^\s*\|?[\s:-|]+\|?\s*$') {
            return $Line
        }
        $prefix = if ($Line.TrimStart().StartsWith("|")) { "|" } else { "" }
        $suffix = if ($Line.TrimEnd().EndsWith("|")) { "|" } else { "" }
        $trimmed = $Line.Trim()
        if ($trimmed.StartsWith("|")) {
            $trimmed = $trimmed.Substring(1)
        }
        if ($trimmed.EndsWith("|")) {
            $trimmed = $trimmed.Substring(0, $trimmed.Length - 1)
        }
        $cells = $trimmed -split "\|"
        $convertedCells = foreach ($cell in $cells) {
            " " + (Convert-InlineMarkdown $cell.Trim()) + " "
        }
        return $prefix + ($convertedCells -join "|") + $suffix
    }
    return Convert-InlineMarkdown $Line
}

function Convert-EmojiTokenToAscii {
    param([string]$Token)
    if ($Token -eq "🍌") {
        return ""
    }
    if ($reverseWordMap.ContainsKey($Token)) {
        return $reverseWordMap[$Token]
    }

    $remaining = $Token
    $decoded = New-Object System.Collections.Generic.List[string]
    while ($remaining.Length -gt 0) {
        $matched = $false
        foreach ($emoji in ($reverseCharMap.Keys | Sort-Object Length -Descending)) {
            if ($remaining.StartsWith($emoji, [System.StringComparison]::Ordinal)) {
                $decoded.Add($reverseCharMap[$emoji])
                $remaining = $remaining.Substring($emoji.Length)
                $matched = $true
                break
            }
        }
        if (-not $matched) {
            return "[unknown:$Token]"
        }
    }
    return ($decoded -join "")
}

function Convert-LineToAscii {
    param([string]$Line)
    $tokens = [regex]::Matches($Line, "\S+")
    $out = New-Object System.Collections.Generic.List[string]
    foreach ($token in $tokens) {
        if ($token.Value -match '^#{1,6}$' -or $token.Value -match '^\d+\.$' -or $token.Value -match '^>+$' -or $token.Value -match '^\|+$' -or $token.Value -match '^-+$' -or $token.Value -match '^`+$') {
            $out.Add($token.Value)
            continue
        }
        $clean = $token.Value.Trim([char[]]@("|", "[", "]", "(", ")", "*", '`', ".", ":", ";", ",", "!", "?"))
        $decoded = Convert-EmojiTokenToAscii $clean
        if ($decoded) {
            $out.Add($decoded)
        }
    }
    return ($out -join " ")
}

$lines = [System.IO.File]::ReadAllLines($InputPath, [System.Text.Encoding]::UTF8)
if ($Direction -eq "AsciiToEmoji") {
    $inFence = $false
    $converted = foreach ($line in $lines) {
        Convert-LineToEmoji $line ([ref]$inFence)
    }
} else {
    $converted = foreach ($line in $lines) {
        Convert-LineToAscii $line
    }
}

$parent = Split-Path -Parent $OutputPath
if ($parent) {
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
}
$utf8Bom = New-Object System.Text.UTF8Encoding($true)
[System.IO.File]::WriteAllLines($OutputPath, [string[]]$converted, $utf8Bom)

