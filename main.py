"""Codyssey 파이썬 퀴즈 게임 - main.py"""


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


def main():
    print("프로그램을 시작합니다.")

    while True:
        show_menu()

        try:
            choice = get_menu_choice()
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
            break

        if choice is None:
            continue

        if choice == 1:
            print("(퀴즈 풀기 기능은 다음 단계에서 구현 예정)")
        elif choice == 2:
            print("(퀴즈 추가 기능은 다음 단계에서 구현 예정)")
        elif choice == 3:
            print("(퀴즈 목록 기능은 다음 단계에서 구현 예정)")
        elif choice == 4:
            print("(점수 확인 기능은 다음 단계에서 구현 예정)")
        elif choice == 5:
            print("프로그램을 종료합니다. 안녕히 가세요!")
            break


if __name__ == "__main__":
    main()