// TODO: 1. 게임 상태를 관리하는 객체를 만든다 ✅
// TODO: 2. DOM을 사용해서 HTML에 있는 id를 가져온다 ✅
// TODO: 3. 게임 시작 시의 초기화 함수를 만든다 ✅
// TODO: 4. 숫자 확인 버튼 이벤트를 작동시키는 함수를 만든다 ✅
// TODO: 5. 스트라이크/볼을 계산하는 함수를 만든다 ✅
// TODO: 6. 결과를 화면에 표시하는 함수를 만든다 ✅
// TODO: 7. 게임 종료를 처리하는 함수를 만든다 ✅

const game = {
  answer: [], // 정답 숫자 3개 (예: [1, 4, 9])
  attempts: 9, // 남은 시도 횟수
  isGameOver: false, // 게임이 끝났는지 여부
}; // TODO 1번 완료

// HTML에서 필요한 id 가져오기
const number1Input = document.getElementById("number1");
const number2Input = document.getElementById("number2");
const number3Input = document.getElementById("number3");
const attemptsSpan = document.getElementById("attempts");
const resultsDiv = document.getElementById("results");
const gameResultImg = document.getElementById("game-result-img");
const submitBtn = document.querySelector(".submit-button"); // TODO 2번 완료

// 게임 시작 시 초기화하는 함수
function initGame() {
  game.answer = [];
  while (game.answer.length < 3) {
    const randomNum = Math.floor(Math.random() * 10); // 0~9 사이의 랜덤 숫자
    if (!game.answer.includes(randomNum)) {
      game.answer.push(randomNum); // 중복이 아니면 추가
    }
  }

  // 게임 상태 초기화
  game.attempts = 9;
  game.isGameOver = false;

  // 화면 초기화
  attemptsSpan.textContent = game.attempts;
  resultsDiv.innerHTML = "";
  gameResultImg.src = "";
  number1Input.value = "";
  number2Input.value = "";
  number3Input.value = "";
  submitBtn.disabled = false;

  // console.log("정답:", game.answer); // 테스트용
}

// 게임 시작할 때 1번 실행
initGame(); // TODO 3번 완료

// 스트라이크와 볼을 계산하는 함수
function calculateResult(userNumbers) {
  let strikes = 0; // 스트라이크 개수
  let balls = 0; // 볼 개수

  // 3개의 숫자를 하나씩 비교
  for (let i = 0; i < 3; i++) {
    if (userNumbers[i] === game.answer[i]) {
      strikes += 1; // 숫자와 위치가 모두 같으면 스트라이크
    }
    else if (game.answer.includes(userNumbers[i])) {
      balls += 1; // 숫자는 있지만 위치가 다르면 볼
    }
  }

  return { strikes: strikes, balls: balls };
} // TODO 5번 완료

// 결과를 화면에 보여주는 함수
function displayResult(userNumbers, strikes, balls) {
  // 새로운 결과 줄 만들기
  const resultRow = document.createElement("div");
  resultRow.className = "check-result";

  // 왼쪽: 입력한 숫자들
  const leftDiv = document.createElement("div");
  leftDiv.className = "left";
  leftDiv.textContent = userNumbers.join(" "); // [1, 2, 3] → 1 2 3

  // 중간: 구분자 ":"
  const colonDiv = document.createElement("div");
  colonDiv.textContent = ":";

  // 오른쪽: 결과 표시
  const rightDiv = document.createElement("div");
  rightDiv.className = "right";

  // 스트라이크도 볼도 없으면 아웃
  if (strikes === 0 && balls === 0) {
    const outSpan = document.createElement("span");
    outSpan.className = "num-result out";
    outSpan.textContent = "O";
    rightDiv.appendChild(outSpan);
  }
  else {
    // 스트라이크가 있으면 표시
    if (strikes > 0) {
      const strikeText = document.createElement("span");
      strikeText.textContent = strikes + " ";
      rightDiv.appendChild(strikeText);

      const strikeSpan = document.createElement("span");
      strikeSpan.className = "num-result strike";
      strikeSpan.textContent = "S";
      rightDiv.appendChild(strikeSpan);

      const space = document.createElement("span");
      space.textContent = " ";
      rightDiv.appendChild(space);
    }

    // 볼 표시
    const ballText = document.createElement("span");
    ballText.textContent = balls + " ";
    rightDiv.appendChild(ballText);

    const ballSpan = document.createElement("span");
    ballSpan.className = "num-result ball";
    ballSpan.textContent = "B";
    rightDiv.appendChild(ballSpan);
  }

  // 왼쪽, 중간, 오른쪽 합치기
  resultRow.appendChild(leftDiv);
  resultRow.appendChild(colonDiv);
  resultRow.appendChild(rightDiv);

  // 최신 결과가 맨 위에 오도록 추가
  resultsDiv.insertBefore(resultRow, resultsDiv.firstChild);
} // TODO 6번 완료

// 게임 종료 처리하는 함수
function endGame(isWin) {
  game.isGameOver = true;

  // 승리/패배 이미지 보여주기
  if (isWin) {
    gameResultImg.src = "success.png";
  }
  else {
    gameResultImg.src = "fail.png";
  }

  submitBtn.disabled = true; // 확인하기 버튼 비활성화
} // TODO 7번 완료

// 확인하기 버튼 클릭 이벤트
function check_numbers() {
  if (game.isGameOver) return; // 게임이 끝났으면 아무것도 안 함

  // 입력한 숫자 가져오기
  const num1 = number1Input.value;
  const num2 = number2Input.value;
  const num3 = number3Input.value;

  // 입력 안 한 칸이 있는지 확인
  if (num1 === "" || num2 === "" || num3 === "") {
    // 입력창만 비우고 종료
    number1Input.value = "";
    number2Input.value = "";
    number3Input.value = "";
    number1Input.focus(); // 첫 번째 칸으로 커서 이동
    return;
  }

  // 입력한 숫자들을 배열로 만들기 (문자에서 숫자로 변환)
  const userNumbers = [parseInt(num1), parseInt(num2), parseInt(num3)];

  const result = calculateResult(userNumbers); // 스트라이크, 볼 계산하기
  const strikes = result.strikes;
  const balls = result.balls;

  displayResult(userNumbers, strikes, balls); // 결과를 화면에 표시

  game.attempts -= 1; // 남은 횟수 1 감소
  attemptsSpan.textContent = game.attempts;

  // 입력창 비우기
  number1Input.value = "";
  number2Input.value = "";
  number3Input.value = "";
  number1Input.focus();

  // 게임 종료 조건 확인
  if (strikes === 3) {
    endGame(true); // 3 스트라이크면 승리
  }
  else if (game.attempts === 0) {
    endGame(false); // 남은 횟수가 0이면 패배
  }
} // TODO 4번 완료

/* 추가 편의 기능 */

// 숫자 입력하면 자동으로 다음 칸으로 이동
number1Input.addEventListener("input", (e) => {
  if (e.target.value.length === 1) {
    number2Input.focus();
  }
});

number2Input.addEventListener("input", (e) => {
  if (e.target.value.length === 1) {
    number3Input.focus();
  }
});

// 백스페이스 누르면 자동으로 전 칸으로 이동
number3Input.addEventListener("keydown", (e) => {
  if (e.key === "Backspace" && e.target.value.length === 1) {
    e.target.value = ""; // 해당 칸에 있는 숫자 지우면서
    number2Input.focus(); // 커서 이동
    e.preventDefault(); // 기본 백스페이스 동작 막기
  }
});

number2Input.addEventListener("keydown", (e) => {
  if (e.key === "Backspace" && e.target.value.length === 1) {
    e.target.value = "";
    number1Input.focus();
    e.preventDefault();
  }
});

// 마지막 칸에서 Enter 누르면 확인하기
number3Input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    check_numbers();
  }
});