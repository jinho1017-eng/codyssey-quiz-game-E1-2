"""QuizGame 클래스 - 게임 전체를 관리한다."""
import random
import json
from pathlib import Path

from quiz import Quiz
from default_quizzes import DEFAULT_QUIZZES

STATE_FILE = Path(__file__).with_name("state.json")


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load_state()

    def load_state(self):
        """state.json에서 퀴즈 데이터와 최고 점수를 불러온다.
        파일이 없거나 손상된 경우 기본 퀴즈 데이터를 사용한다."""
        if not STATE_FILE.exists():
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            self.best_score = data.get("best_score")
            score_text = self.best_score if self.best_score is not None else "없음"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})")
        except (json.JSONDecodeError, KeyError, OSError):
            print("⚠️ 저장된 데이터 파일이 손상되었습니다. 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None

    def save_state(self):
        """현재 퀴즈 데이터와 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"⚠️ 데이터 저장에 실패했습니다: {error}")

    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def get_menu_choice(self):
        """메뉴 번호(1~5)를 입력받아 반환한다. 형식이 잘못됐으면 None을 반환한다."""
        raw = input("선택: ")
        value = raw.strip()

        if value == "":
            print("⚠️ 아무것도 입력하지 않으셨습니다. 다시 입력해주세요.")
            return None

        if not value.isdigit():
            print("⚠️ 잘못된 입력입니다. 숫자를 입력하세요.")
            return None

        choice = int(value)
        if choice < 1 or choice > 5:
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            return None

        return choice

    def get_answer_choice(self):
        """정답 번호(1~4)를 입력받아 반환한다. 형식이 잘못됐으면 None을 반환한다."""
        raw = input("정답 입력: ")
        value = raw.strip()

        if value == "":
            print("⚠️ 아무것도 입력하지 않으셨습니다. 다시 입력해주세요.")
            return None

        if not value.isdigit():
            print("⚠️ 잘못된 입력입니다. 숫자를 입력하세요.")
            return None

        choice = int(value)
        if choice < 1 or choice > 4:
            print("⚠️ 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
            return None

        return choice

    def get_nonempty_text(self, prompt):
        """빈 값이 아닌 텍스트를 입력받는다."""
        while True:
            raw = input(prompt)
            value = raw.strip()
            if value == "":
                print("⚠️ 아무것도 입력하지 않으셨습니다. 다시 입력해주세요.")
                continue
            return value

    def get_question_count(self):
        """풀 문제 수를 입력받는다. 빈 입력이면 전체 문제 수를 사용한다."""
        total = len(self.quizzes)
        while True:
            raw = input(f"몇 문제를 푸시겠습니까? (1~{total}, 그냥 Enter는 전체 {total}문제): ")
            value = raw.strip()

            if value == "":
                return total

            if not value.isdigit():
                print("⚠️ 잘못된 입력입니다. 숫자를 입력하세요.")
                continue

            count = int(value)
            if count < 1 or count > total:
                print(f"⚠️ 잘못된 입력입니다. 1-{total} 사이의 숫자를 입력하세요.")
                continue

            return count

    def play_quiz(self):
        """퀴즈 목록을 출제하고 점수를 계산해 반환한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return None
        count = self.get_question_count()

        print(f"\n📝 퀴즈를 시작합니다! (총 {count}문제)")

        quizzes_to_play = random.sample(self.quizzes, count)
        correct_count = 0
        for index, quiz in enumerate(quizzes_to_play, start=1):
            print("-" * 40)
            print(f"[문제 {index}]")
            quiz.show()

            answer = None
            while answer is None:
                answer = self.get_answer_choice()

            if quiz.is_correct(answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = int(correct_count / len(self.quizzes) * 100)
        print("=" * 40)
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {correct_count}문제 정답! ({score}점)")
        print("=" * 40)
        return score

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가하고 파일에 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")

        question = self.get_nonempty_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = self.get_nonempty_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = None
        while answer is None:
            answer = self.get_answer_choice()

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈 목록을 출력한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("-" * 40)

    def check_score(self):
        """최고 점수를 출력한다."""
        if self.best_score is None:
            print("\n아직 퀴즈를 풀지 않으셨습니다. 먼저 퀴즈를 풀어보세요.")
            return

        print(f"\n🏆 최고 점수: {self.best_score}점")

    def run(self):
        """게임의 메인 루프를 실행한다."""
        print("프로그램을 시작합니다.")

        while True:
            self.show_menu()

            try:
                choice = self.get_menu_choice()

                if choice is None:
                    continue

                if choice == 1:
                    score = self.play_quiz()
                    if score is not None and (self.best_score is None or score > self.best_score):
                        self.best_score = score
                        self.save_state()
                        print("🎉 새로운 최고 점수입니다!")
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.check_score()
                elif choice == 5:
                    print("프로그램을 종료합니다. 안녕히 가세요!")
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
                self.save_state()
                break