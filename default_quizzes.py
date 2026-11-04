"""기본 퀴즈 데이터 - Python 상식 퀴즈."""

from quiz import Quiz

DEFAULT_QUIZZES = [
    Quiz("Python의 창시자는 누구인가?",
         ["Guido van Rossum", "Dennis Ritchie", "James Gosling", "Brendan Eich"],
         1),
    Quiz("다음 중 Python에서 값을 변경할 수 없는(immutable) 자료형은?",
         ["list", "dict", "tuple", "set"],
         3),
    Quiz("여러 값을 '키: 값' 쌍으로 저장하는 Python 자료형은?",
         ["list", "tuple", "dict", "str"],
         3),
    Quiz("Python에서 코드 블록(함수, if문 등)을 구분하는 기준은?",
         ["중괄호 {}", "들여쓰기(indentation)", "세미콜론(;)", "begin/end 키워드"],
         2),
    Quiz("Python 소스 파일의 일반적인 확장자는?",
         [".pt", ".pyt", ".py", ".python"],
         3),
    Quiz("다음 중 Python의 반복문 키워드는?",
         ["foreach", "for", "loop", "repeat"],
         2),
]