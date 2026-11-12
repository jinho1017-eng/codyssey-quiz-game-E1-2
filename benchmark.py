"""1000개 이상 데이터에 대한 성능/메모리 측정 스크립트 (1회 실행용, 실제 state.json 사용 안 함)."""
import sys
import time
import tempfile
import tracemalloc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import quiz_game
from quiz_game import QuizGame
from quiz import Quiz


def make_dummy_quizzes(count):
    """count개의 더미 퀴즈를 생성한다."""
    return [
        Quiz(f"더미 문제 {i}번", ["선택1", "선택2", "선택3", "선택4"], (i % 4) + 1)
        for i in range(count)
    ]


def main():
    tmp_dir = Path(tempfile.mkdtemp())
    quiz_game.STATE_FILE = tmp_dir / "state.json"
    quiz_game.BACKUP_FILE = tmp_dir / "state.json.bak"

    game = QuizGame()
    game.quizzes = make_dummy_quizzes(1000)
    game.best_score = 80

    tracemalloc.start()

    start = time.perf_counter()
    game.save_state()
    save_time = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    game2 = QuizGame()
    load_time = (time.perf_counter() - start) * 1000

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"퀴즈 개수: {len(game.quizzes)}개")
    print(f"저장(save_state) 시간: {save_time:.2f} ms")
    print(f"불러오기(재시작) 시간: {load_time:.2f} ms")
    print(f"측정 구간 피크 메모리: {peak / 1024:.1f} KB")


if __name__ == "__main__":
    main()