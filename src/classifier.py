import re
from urllib import parse
import logging

BAD_WORDS = [
    'sleep', 'drop', 'uid', 'uname', 'select', 'waitfor', 'delay', 'system', 'union', 'order by', 'group by',
    'information_schema', 'load_file', 'outfile', 'dumpfile', 'into', 'exec', 'char', 'nchar', 'varchar', 'nvarchar',
    'cast', 'convert'
]

SQL_PATTERNS = [
    r"(?i)\bselect\b.*\bfrom\b", r"(?i)\bunion\b.*\bselect\b", r"(?i)\binsert\b.*\binto\b",
    r"(?i)\bupdate\b.*\bset\b", r"(?i)\bdelete\b.*\bfrom\b", r"(?i)\bdrop\b.*\btable\b",
    r"(?i)\bcreate\b.*\btable\b", r"(?i)\balter\b.*\btable\b", r"(?i)\btruncate\b.*\btable\b",
    r"(?i)\bexec\b", r"(?i)\bchar\b", r"(?i)\bnchar\b", r"(?i)\bvarchar\b", r"(?i)\bnvarchar\b",
    r"(?i)\bcast\b", r"(?i)\bconvert\b", r"(?i)\binto\b.*\boutfile\b", r"(?i)\binto\b.*\bdumpfile\b",
    r"(?i)\binformation_schema\b", r"(?i)\bselect\b.*\bfrom\b.*\bwhere\b", r"(?i)\b--\b", r"(?i)\b#\b",
    r"(?i)\b;\b", r"(?i)\b--\b", r"(?i)\b' OR\b", r"(?i)\b' AND\b", r"(?i)\bOR '1'='1'\b", r"(?i)\bAND '1'='1'\b"
]

def ExtractFeatures(path, body=""):
    path = parse.unquote(path)
    body = parse.unquote(body)
    combined = path + " " + body
    combined_lower = combined.lower()

    single_q = combined.count("'")
    double_q = combined.count('"')
    dashes = combined.count('--')
    braces = combined.count('(')
    spaces = combined.count(' ')

    badwords_count = sum(combined.count(word) for word in BAD_WORDS)
    sql_patterns_count = sum(len(re.findall(pattern, combined_lower)) for pattern in SQL_PATTERNS)

    features = {
        'single_q': single_q,
        'double_q': double_q,
        'dashes': dashes,
        'braces': braces,
        'spaces': spaces,
        'badwords_count': badwords_count,
        'sql_patterns_count': sql_patterns_count
    }
    logging.info(f'Extracted features: {features}')
    return features

def classify_query(features):
    if features['badwords_count'] > 0 or features['sql_patterns_count'] > 0:
        return "Bad"
    return "Good"
