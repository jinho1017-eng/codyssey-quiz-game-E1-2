"""Codyssey 파이썬 퀴즈 게임 - main.py"""

from default_quizzes import DEFAULT_QUIZZES


def show_menu():
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def get_menu_choice():
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


def get_answer_choice():
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


def play_quiz(quizzes):
    """퀴즈 목록을 출제하고 점수를 계산해 반환한다."""
    if not quizzes:
        print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
        return None

    print(f"\n📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)")

    correct_count = 0
    for index, quiz in enumerate(quizzes, start=1):
        print("-" * 40)
        print(f"[문제 {index}]")
        quiz.show()

        answer = None
        while answer is None:
            answer = get_answer_choice()

        if quiz.is_correct(answer):
            print("✅ 정답입니다!")
            correct_count += 1
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

    score = int(correct_count / len(quizzes) * 100)
    print("=" * 40)
    print(f"🏆 결과: {len(quizzes)}문제 중 {correct_count}문제 정답! ({score}점)")
    print("=" * 40)
    return score


def main():
    print("프로그램을 시작합니다.")

    while True:
        show_menu()

        try:
            choice = get_menu_choice()

            if choice is None:
                continue

            if choice == 1:
                play_quiz(DEFAULT_QUIZZES)
            elif choice == 2:
                print("(퀴즈 추가 기능은 다음 단계에서 구현 예정)")
            elif choice == 3:
                print("(퀴즈 목록 기능은 다음 단계에서 구현 예정)")
            elif choice == 4:
                print("(점수 확인 기능은 다음 단계에서 구현 예정)")
            elif choice == 5:
                print("프로그램을 종료합니다. 안녕히 가세요!")
                break
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
            break


if __name__ == "__main__":
    main()