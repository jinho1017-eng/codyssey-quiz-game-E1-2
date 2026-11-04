"""Quiz 클래스 - 퀴즈 1개를 표현한다."""


class Quiz:
    def __init__(self, question, choices, answer, hint=None):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def show(self):
        """문제와 선택지를 출력한다."""
        print(f"\n문제: {self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 입력한 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리로부터 Quiz 객체를 생성한다."""
        return cls(data["question"], data["choices"], data["answer"], data.get("hint"))