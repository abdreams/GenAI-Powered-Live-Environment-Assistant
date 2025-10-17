"""
Code Mapper - Maps error logs and stack traces to actual code
"""
import os
import re
from typing import Dict, List, Optional
from pathlib import Path


class CodeMapper:
    """Maps errors from logs to specific code locations"""
    
    def __init__(self, codebase_dir: str):
        self.codebase_dir = codebase_dir
        self.file_cache = {}
        self._load_codebase()
    
    def _load_codebase(self):
        """Load all Python files from the codebase into memory"""
        codebase_path = Path(self.codebase_dir)
        
        if not codebase_path.exists():
            return
        
        for file_path in codebase_path.glob("**/*.py"):
            with open(file_path, 'r') as f:
                # Store with path relative to project root (includes dummy_data/codebase/)
                relative_path = str(file_path.relative_to(codebase_path.parent.parent))
                self.file_cache[relative_path] = {
                    'content': f.read(),
                    'lines': open(file_path, 'r').readlines()
                }
    
    def extract_stack_trace(self, log_content: str) -> List[Dict]:
        """
        Extract stack trace information from log content
        
        Returns:
            List of dicts with file, line, and function information
        """
        stack_trace = []
        
        # Pattern to match Python stack trace lines
        # Example: File "/app/dummy_data/codebase/database_manager.py", line 91, in execute_transaction
        pattern = r'File "([^"]+)", line (\d+)(?:, in (.+))?'
        
        matches = re.finditer(pattern, log_content)
        
        for match in matches:
            file_path = match.group(1)
            line_num = int(match.group(2))
            function_name = match.group(3) if match.group(3) else None
            
            # Normalize path
            normalized_path = self._normalize_path(file_path)
            
            stack_trace.append({
                'file': normalized_path,
                'line': line_num,
                'function': function_name,
                'original_path': file_path
            })
        
        return stack_trace
    
    def _normalize_path(self, path: str) -> str:
        """Normalize file path to match our codebase structure"""
        # Remove /app/ prefix if present
        path = path.replace('/app/', '')
        return path
    
    def get_code_context(self, file_path: str, line_num: int, 
                        context_lines: int = 5) -> Optional[Dict]:
        """
        Get code context around a specific line
        
        Args:
            file_path: Path to the file
            line_num: Line number (1-indexed)
            context_lines: Number of lines before and after to include
            
        Returns:
            Dict with code snippet and metadata
        """
        if file_path not in self.file_cache:
            return None
        
        lines = self.file_cache[file_path]['lines']
        total_lines = len(lines)
        
        # Calculate range (convert to 0-indexed)
        start = max(0, line_num - context_lines - 1)
        end = min(total_lines, line_num + context_lines)
        
        # Get the code snippet
        snippet_lines = []
        for i in range(start, end):
            line_text = lines[i].rstrip()
            is_error_line = (i == line_num - 1)
            snippet_lines.append({
                'line_num': i + 1,
                'content': line_text,
                'is_error': is_error_line
            })
        
        return {
            'file': file_path,
            'error_line': line_num,
            'snippet': snippet_lines,
            'start_line': start + 1,
            'end_line': end
        }
    
    def find_function_definition(self, file_path: str, function_name: str) -> Optional[Dict]:
        """Find the definition of a function in a file"""
        if file_path not in self.file_cache:
            return None
        
        lines = self.file_cache[file_path]['lines']
        
        # Pattern to match function definitions
        pattern = rf'^\s*def {re.escape(function_name)}\s*\('
        
        for i, line in enumerate(lines):
            if re.match(pattern, line):
                return {
                    'file': file_path,
                    'function': function_name,
                    'line': i + 1,
                    'definition': line.strip()
                }
        
        return None
    
    def map_error_to_code(self, log_content: str) -> Dict:
        """
        Map error log to code locations with context
        
        Returns:
            Dict with error analysis and code mappings
        """
        # Extract stack trace
        stack_trace = self.extract_stack_trace(log_content)
        
        if not stack_trace:
            return {
                'error': 'No stack trace found in log',
                'stack_trace': [],
                'code_contexts': []
            }
        
        # Get code context for each frame
        code_contexts = []
        for frame in stack_trace:
            context = self.get_code_context(frame['file'], frame['line'])
            if context:
                context['function'] = frame['function']
                code_contexts.append(context)
        
        # Extract error message
        error_pattern = r'(Exception|Error): (.+?)(?:\n|$)'
        error_match = re.search(error_pattern, log_content)
        error_message = error_match.group(0) if error_match else "Unknown error"
        
        return {
            'error_message': error_message,
            'stack_trace': stack_trace,
            'code_contexts': code_contexts,
            'root_cause_file': stack_trace[-1]['file'] if stack_trace else None,
            'root_cause_line': stack_trace[-1]['line'] if stack_trace else None,
            'root_cause_function': stack_trace[-1]['function'] if stack_trace else None
        }
    
    def get_all_files(self) -> List[str]:
        """Get list of all files in the codebase"""
        return list(self.file_cache.keys())
    
    def get_file_content(self, file_path: str) -> Optional[str]:
        """Get full content of a file"""
        if file_path in self.file_cache:
            return self.file_cache[file_path]['content']
        return None
