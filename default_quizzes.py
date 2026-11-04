"""기본 퀴즈 데이터 - Python 상식 퀴즈."""

from quiz import Quiz

DEFAULT_QUIZZES = [
    Quiz("Python의 창시자는 누구인가?",
         ["Guido van Rossum", "Dennis Ritchie", "James Gosling", "Brendan Eich"],
         1,
         hint="네덜란드 출신 프로그래머이며, 1991년에 Python을 처음 발표했습니다."),
    Quiz("다음 중 Python에서 값을 변경할 수 없는(immutable) 자료형은?",
         ["list", "dict", "tuple", "set"],
         3,
         hint="한 번 만들어지면 내부 값을 바꿀 수 없어서, 고정된 데이터를 다룰 때 주로 씁니다."),
    Quiz("여러 값을 '키: 값' 쌍으로 저장하는 Python 자료형은?",
         ["list", "tuple", "dict", "str"],
         3,
         hint="사전에서 단어를 찾듯이, '키'로 '값'을 빠르게 찾을 수 있는 구조입니다."),
    Quiz("Python에서 코드 블록(함수, if문 등)을 구분하는 기준은?",
         ["중괄호 {}", "들여쓰기(indentation)", "세미콜론(;)", "begin/end 키워드"],
         2,
         hint="같은 블록에 속한 코드는 줄 앞의 빈 칸 개수를 똑같이 맞춰야 합니다."),
    Quiz("Python 소스 파일의 일반적인 확장자는?",
         [".pt", ".pyt", ".py", ".python"],
         3,
         hint="이 확장자가 붙은 파일은 별도 컴파일 없이 인터프리터로 바로 실행할 수 있습니다."),
    Quiz("다음 중 Python의 반복문 키워드는?",
         ["foreach", "for", "loop", "repeat"],
         2,
         hint="C, Java 등 다른 여러 언어에도 같은 이름의 반복문이 있습니다."),
]