const user = 'player1';

async function updateBalance() {
  const res = await fetch(`/balance/${user}`);
  const data = await res.json();
  document.getElementById('balance').textContent = data.balance;
}

async function deposit(amount=20) {
  await fetch(`/deposit/${user}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount })
  });
  updateBalance();
}

document.getElementById('spin').addEventListener('click', async () => {
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const oscillator = audioCtx.createOscillator();
  oscillator.frequency.value = 440;
  oscillator.connect(audioCtx.destination);
  oscillator.start();
  oscillator.stop(audioCtx.currentTime + 0.1);

  const res = await fetch('/spin/fireball_frenzy', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user, cost: 1 })
  });
  const data = await res.json();

  if (data.error) {
    document.getElementById('result').textContent = data.error;
  } else {
    let msg = data.win ? 'WIN!' : 'Try again';
    if (data.jackpot) {
      msg += ` - ${data.jackpot.toUpperCase()} JACKPOT!`;
    }
    document.getElementById('result').textContent = msg;
    updateBalance();
  }
});

// Seed some starting tokens on first load
window.addEventListener('load', () => {
  deposit(10);
});
