let playerStatus = [
    [0, 0, 0, 0], // Situation 1
    [0, 0, 0, 0], // Situation 2
    [0, 0, 0, 0], // Situation 3
    [0, 0, 0, 0]  // Cumulative Status
];

function handleChoice(situation, choice) {
    switch (situation) {
        case 1:
            if (choice === 'yes') {
                playerStatus[0] = [1, 3, 3, 6];
            }
            break;

        case 2:
            if (choice === 'yes') {
                playerStatus[1] = [-2, -2, -1, -3];
            }
            break;

        case 3:
            if (choice === '1') {
                playerStatus[2] = [2, 0, 1, 3];
            } else if (choice === '2') {
                playerStatus[2] = [0, 3, 2, 4];
            } else if (choice === '3') {
                playerStatus[2] = [0, 3, 5, 1];
            }
            break;
    }

    // Show the next situation or the result
    if (situation === 1) {
        document.getElementById('situation1').style.display = 'none';
        document.getElementById('situation2').style.display = 'block';
    } else if (situation === 2) {
        document.getElementById('situation2').style.display = 'none';
        document.getElementById('situation3').style.display = 'block';
    } else if (situation === 3) {
        document.getElementById('situation3').style.display = 'none';
        showResult();
    }
}

function showResult() {
    // Calculate cumulative status
    for (let i = 0; i < 4; i++) {
        playerStatus[3][i] = playerStatus[0][i] + playerStatus[1][i] + playerStatus[2][i];
    }

    // Display the result
    document.getElementById('result').style.display = 'block';
    document.getElementById('status').innerText =
        `Situation 1: ${playerStatus[0].join(', ')}\n` +
        `Situation 2: ${playerStatus[1].join(', ')}\n` +
        `Situation 3: ${playerStatus[2].join(', ')}\n` +
        `Final Status: ${playerStatus[3].join(', ')}`;
}
