# src/vogon_poetry/__init__.py
from typing import Dict, Optional, List


class VogonPoet:
    """A daemon that dreams in working code. Visions are bold and strange but COMPILE."""
    
    VOCATIVES = {
        "Oh": ["I", "Thee"],
        "Thy": ["Heinrichs", "His"],
        "Frostled Gruntbuggly": ["Gruntbuggly Frosted", "Gruftly Buggles of the Cold"],
    }

    def __init__(self):
        self.vocatives: Dict[str, List[str]] = {}

    def add_vocabulary(self, word: str) -> None:
        """Add a vocative phrase to the dictionary."""
        if word not in self.VOCATIVES:
            self.VOCATIVES[word] = []
        
        # Add common variants for better poetic effect
        base_variants = [word + "s", word, f"{word}th"]
        remaining_words = set(self.VOCATIVES[w].copy() if w in self else []) - set(base_variants)
        self.add_vocatives(remaining_words)

    def generate_poetic_code(self, text: str) -> List[str]:
        """Generate valid Python code from lorem ipsum-like text."""
        
        # 1. Parse stanza boundaries (simple regex for test purposes in this demo)
        lines = [line.rstrip() for line in text.split('\n') if line.strip()]
        
        poems = []

        def parse_stanza(line: str, current_poem_index: int):
            """Parse a single stanza into words."""
            # Extract potential rhyming pairs based on the poem structure
            rhyme_pairs = [i for i in range(len(lines) - 1)]
            
            if len(rhyme_pairs) == 0 or lines[current_poem_index] not in self.VOCATIVES:
                return []

            words_in_stanza = set()
            current_word_idx = 0
            
            # Process the stanza line by line to find rhyming pairs and word boundaries
            for i, char in enumerate(line):
                if char.isalpha():
                    words_in_stange.add(char)
                
                if len(words_in_stange) == 1:
                    current_word_idx = i
                    
                elif (i - current_word_idx) % 2 == 0 and lines[i] not in self.VOCATIVES:
                    # Check for rhyme at the end of line or start of next line
                    potential_rhyme_end = len(line.rstrip()) + 1 if char.isalpha() else i
                    
                    words_in_stange.add(lines[potential_rhyme_end])
                    
                current_word_idx += 1
                
            return list(words_in_stange)

        # Generate each stanza and append to poems
        for poem_index, lines in enumerate(lines):
            stanza_words = parse_stanza(line.strip(), poem_index)
            
            if not stanza_words:
                continue
            
            # Create a valid Python string representation of the stanza with formatting quirks preserved (simulated here by using raw strings or specific syntax where appropriate)
            poem_lines = []
            for word in stanza_words[:10]:  # Limit to first 10 words per poem block to keep code concise and readable
                if isinstance(word, str):
                    poem_lines.append(f'"""{word}"""')
                
                elif len(stanza_words) > 1:
                    # Use specific formatting for multi-word lines (e.g., single quotes or double spacing in a string literal context would go here, but we'll stick to standard repr style as per "COMPILE" requirement of valid syntax)
                    poem_lines.append(f'"""{word}"""\n')

            poems.append('\n'.join(poem_lines))
        
        return poems
    
    def run_poetry_generation(self, poem_text: str) -> List[str]:
        """Run the generation process on provided text."""
        try:
            lines = [line.rstrip() for line in poem_text.split('\n') if line.strip()]
            
            # Apply vocative substitution logic directly to words found during parsing
            poems = []

            def substitute_vocatives(line: str, current_poem_index: int) -> List[str]:
                """Substitute specific phrases from VOCATIVES with their variants."""
                result = list()
                
                for line_idx in range(len(lines)):
                    if lines[line_idx].lower() not in self.VOCATIVES and (line_idx + 1 < len(lines)) and (lines[line_idx] or lines[line_idx+1]).isalpha():
                        # Find the rhyme pair to substitute
                        rhyming
