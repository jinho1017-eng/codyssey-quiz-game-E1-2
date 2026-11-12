"""QuizGame 클래스 - 게임 전체를 관리한다."""
import random
import json
import shutil
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from quiz import Quiz
from default_quizzes import DEFAULT_QUIZZES

STATE_FILE = Path(__file__).with_name("state.json")
BACKUP_FILE = STATE_FILE.with_name(STATE_FILE.name + ".bak")


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.history = []
        self.load_state()

    def load_state(self):
        """state.json을 읽는다. 손상되었으면 state.json.bak을 시도하고,
        그것도 안 되면 기본 퀴즈 데이터·초기 점수·빈 기록으로 시작한다."""
        if STATE_FILE.exists():
            try:
                self.quizzes, self.best_score, self.history = self._load_from(STATE_FILE)
                score_text = self.best_score if self.best_score is not None else "없음"
                print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})")
                return
            except (json.JSONDecodeError, OSError, ValueError) as error:
                print(f"⚠️ 저장된 데이터 파일이 손상되었습니다 ({error}).")

        if BACKUP_FILE.exists():
            try:
                self.quizzes, self.best_score, self.history = self._load_from(BACKUP_FILE)
                print(f"♻️ 백업 파일({BACKUP_FILE.name})에서 복구했습니다. (퀴즈 {len(self.quizzes)}개)")
                return
            except (json.JSONDecodeError, OSError, ValueError) as error:
                print(f"⚠️ 백업 파일도 손상되었습니다 ({error}).")

        print("기본 퀴즈 데이터로 시작합니다.")
        self.quizzes = list(DEFAULT_QUIZZES)
        self.best_score = None
        self.history = []
        
    @staticmethod
    def _parse_state(data):
        """불러온 JSON 데이터의 구조와 값을 검증해 (quizzes, best_score, history)를 반환한다.
        구조나 값이 올바르지 않으면 ValueError를 발생시킨다."""
        if not isinstance(data, dict):
            raise ValueError("최상위 데이터가 객체(dict)가 아닙니다")

        raw_quizzes = data.get("quizzes")
        if not isinstance(raw_quizzes, list):
            raise ValueError("'quizzes'가 리스트가 아닙니다")

        quizzes = [QuizGame._parse_quiz_item(item) for item in raw_quizzes]

        best_score = data.get("best_score")
        if best_score is not None and (
            not isinstance(best_score, int)
            or isinstance(best_score, bool)
            or not (0 <= best_score <= 100)
        ):
            raise ValueError("'best_score'가 올바른 값이 아닙니다")

        raw_history = data.get("history", [])
        if not isinstance(raw_history, list):
            raise ValueError("'history'가 리스트가 아닙니다")

        history = [QuizGame._parse_history_entry(entry) for entry in raw_history]

        return quizzes, best_score, history

    @staticmethod
    def _parse_quiz_item(item):
        """퀴즈 1개의 딕셔너리를 검증하고 Quiz 객체로 변환한다."""
        if not isinstance(item, dict):
            raise ValueError("퀴즈 항목이 객체(dict)가 아닙니다")

        question = item.get("question")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("퀴즈의 'question'이 올바르지 않습니다")

        choices = item.get("choices")
        if (
            not isinstance(choices, list)
            or len(choices) != 4
            or not all(isinstance(c, str) and c.strip() for c in choices)
        ):
            raise ValueError("퀴즈의 'choices'는 문자열 4개여야 합니다")

        answer = item.get("answer")
        if not isinstance(answer, int) or isinstance(answer, bool) or not (1 <= answer <= 4):
            raise ValueError("퀴즈의 'answer'는 1~4 사이의 정수여야 합니다")

        hint = item.get("hint")
        if hint is not None and not isinstance(hint, str):
            raise ValueError("퀴즈의 'hint'는 문자열이거나 없어야 합니다")

        return Quiz(question, choices, answer, hint)

    @staticmethod
    def _parse_history_entry(entry):
        """게임 기록 1개의 딕셔너리를 검증하고 그대로 반환한다."""
        if not isinstance(entry, dict):
            raise ValueError("게임 기록 항목이 객체(dict)가 아닙니다")

        datetime_value = entry.get("datetime")
        if not isinstance(datetime_value, str) or not datetime_value.strip():
            raise ValueError("게임 기록의 'datetime'이 올바르지 않습니다")

        question_count = entry.get("question_count")
        if (
            not isinstance(question_count, int)
            or isinstance(question_count, bool)
            or question_count < 1
        ):
            raise ValueError("게임 기록의 'question_count'가 올바르지 않습니다")
        

        score = entry.get("score")
        if not isinstance(score, int) or isinstance(score, bool) or not (0 <= score <= 100):
            raise ValueError("게임 기록의 'score'가 올바르지 않습니다")

        return {"datetime": datetime_value, "question_count": question_count, "score": score}

    @staticmethod
    def _load_from(path):
        """path의 JSON을 읽고 검증해 (quizzes, best_score, history)를 반환한다."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return QuizGame._parse_state(data)
    
    def save_state(self):
        """현재 데이터를 저장하고 성공 여부를 반환한다.
        저장 전 기존 state.json이 있으면 state.json.bak으로 백업한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        temp_path = None

        try:
            if STATE_FILE.exists():
                shutil.copyfile(STATE_FILE, BACKUP_FILE)

            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=STATE_FILE.parent,
                suffix=".tmp",
                delete=False,
            ) as file:
                temp_path = Path(file.name)
                json.dump(data, file, ensure_ascii=False, indent=2)

            temp_path.replace(STATE_FILE)
            return True
        except OSError as error:
            print(f"⚠️ 데이터 저장에 실패했습니다: {error}")
            return False
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink(missing_ok=True)
                except OSError:
                    pass


    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 40)

    def get_menu_choice(self):
        """1~6 범위의 정수를 입력받는다. 잘못된 입력이면 None을 반환한다."""
        value = input("선택: ").strip()

        if value == "":
            print("⚠️ 아무것도 입력하지 않으셨습니다. 다시 입력해주세요.")
            return None

        try:
            choice = int(value)
        except ValueError:
            print("⚠️ 잘못된 입력입니다. 숫자를 입력하세요.")
            return None

        if not 1 <= choice <= 6:
            print("⚠️ 잘못된 입력입니다. 1-6 사이의 숫자를 입력하세요.")
            return None

        return choice

    def get_answer_choice(self):
        """1~4 범위의 정수를 입력받는다. 잘못된 입력이면 None을 반환한다."""
        value = input("정답 입력: ").strip()

        if value == "":
            print("⚠️ 아무것도 입력하지 않으셨습니다. 다시 입력해주세요.")
            return None

        try:
            choice = int(value)
        except ValueError:
            print("⚠️ 잘못된 입력입니다. 숫자를 입력하세요.")
            return None

        if not 1 <= choice <= 4:
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

            try:
                count = int(value)
            except ValueError:
                print("⚠️ 잘못된 입력입니다. 숫자를 입력하세요.")
                continue
            if count < 1 or count > total:
                print(f"⚠️ 잘못된 입력입니다. 1-{total} 사이의 숫자를 입력하세요.")
                continue

            return count

    def get_answer_or_hint(self):
        """정답 번호(1~4)를 입력받는다. 'h'를 입력하면 'HINT' 문자열을 반환한다."""
        raw = input("정답 입력 (힌트를 보려면 h 입력): ")
        value = raw.strip()

        if value.lower() == "h":
            return "HINT"

        if value == "":
            print("⚠️ 아무것도 입력하지 않으셨습니다. 다시 입력해주세요.")
            return None

        try:
            choice = int(value)
        except ValueError:
            print("⚠️ 잘못된 입력입니다. 숫자 또는 h를 입력하세요.")
            return None
        if choice < 1 or choice > 4:
            print("⚠️ 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
            return None

        return choice

    def play_quiz(self):
        """퀴즈를 랜덤 순서로 출제하고 (점수, 문제 수)를 반환한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return None, None

        count = self.get_question_count()

        print(f"\n📝 퀴즈를 시작합니다! (총 {count}문제)")

        quizzes_to_play = random.sample(self.quizzes, count)

        correct_count = 0
        hint_used_count = 0
        for index, quiz in enumerate(quizzes_to_play, start=1):
            print("-" * 40)
            print(f"[문제 {index}]")
            quiz.show()

            used_hint = False
            answer = None
            while answer is None:
                if quiz.hint:
                    result = self.get_answer_or_hint()
                    if result == "HINT":
                        print(f"💡 힌트: {quiz.hint}")
                        used_hint = True
                        continue
                    answer = result
                else:
                    answer = self.get_answer_choice()

            if used_hint:
                hint_used_count += 1

            if quiz.is_correct(answer):
                message = "✅ 정답입니다!"
                if used_hint:
                    message += " (힌트 사용 -5점)"
                print(message)
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        raw_score = correct_count * 100 // count
        score = max(0, raw_score - hint_used_count * 5)
        print("=" * 40)
        print(f"🏆 결과: {count}문제 중 {correct_count}문제 정답! ({score}점)")
        if hint_used_count:
            print(f"   (힌트 {hint_used_count}회 사용으로 {hint_used_count * 5}점 감점됨)")
        print("=" * 40)
        return score, count

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

        hint_raw = input("힌트를 입력하세요 (선택사항, 없으면 그냥 Enter): ")
        hint = hint_raw.strip() if hint_raw.strip() else None

        new_quiz = Quiz(question, choices, answer, hint=hint)
        self.quizzes.append(new_quiz)
        if self.save_state():
            print("\n✅ 퀴즈를 추가하고 저장했습니다.")
        else:
            print("\n⚠️ 퀴즈는 현재 실행 중인 목록에만 추가됐습니다.")

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

    def delete_quiz(self):
        """등록된 퀴즈를 번호로 선택해 삭제하고 파일에 저장한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        self.list_quizzes()

        index = None
        while index is None:
            raw = input("삭제할 퀴즈 번호를 입력하세요: ")
            value = raw.strip()

            if value == "":
                print("⚠️ 아무것도 입력하지 않으셨습니다. 다시 입력해주세요.")
                continue

            try:
                candidate = int(value)
            except ValueError:
                print("⚠️ 잘못된 입력입니다. 숫자를 입력하세요.")
                continue
            if candidate < 1 or candidate > len(self.quizzes):
                print(f"⚠️ 잘못된 입력입니다. 1-{len(self.quizzes)} 사이의 숫자를 입력하세요.")
                continue

            index = candidate

        removed = self.quizzes.pop(index - 1)
        if self.save_state():
            print(f"\n🗑️ 퀴즈를 삭제하고 저장했습니다: {removed.question}")
        else:
            print(f"\n⚠️ 퀴즈는 현재 실행 중인 목록에서만 삭제됐습니다: {removed.question}")

    def check_score(self):
        """최고 점수와 최근 게임 기록을 출력한다."""
        if self.best_score is None:
            print("\n아직 퀴즈를 풀지 않으셨습니다. 먼저 퀴즈를 풀어보세요.")
            return

        print(f"\n🏆 최고 점수: {self.best_score}점")

        if self.history:
            print("\n📜 최근 게임 기록 (최대 5개):")
            for entry in self.history[-5:]:
                print(f"  {entry['datetime']} | {entry['question_count']}문제 | {entry['score']}점")

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
                    score, count = self.play_quiz()
                    if score is not None:
                        self.history.append({
                            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "question_count": count,
                            "score": score,
                        })
                        if self.best_score is None or score > self.best_score:
                            self.best_score = score
                            print("🎉 새로운 최고 점수입니다!")
                        self.save_state()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.check_score()
                elif choice == 5:
                    self.delete_quiz()
                elif choice == 6:
                    print("프로그램을 종료합니다. 안녕히 가세요!")
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
                self.save_state()
                break