let blocks = Array.from({length: 22}, (_, i) => i + 1).map(num => num.toString());
let [milliseconds,seconds] = [0,0];
let timerRef = document.querySelector('.timerDisplay');
let nIntervId;
let currentTime = 0;
let timeDiff = 0;
let lastTime = 0;
let pointAnalytics = [];
let points = 0;
let busts = 0;

function resetResults() {
clearInterval(nIntervId);
[milliseconds,seconds] = [0,0];
timerRef = document.querySelector('.timerDisplay');
nIntervId = null;
currentTime = 0;
timeDiff = 0;
lastTime = 0;
points = 0;
busts = 0;
timerRef.innerHTML = "00 : 000";
updatePoints();
const myNode = document.getElementById("table-results").getElementsByTagName('tbody')[0];
myNode.innerHTML = "";
pointAnalytics = [];
}

function getVideoId(url) {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);

    return (match && match[2].length === 11)
      ? match[2]
      : null;
}


document.getElementById("url-input").addEventListener('input', (e)=>{
document.getElementById("video-iframe").src = "https://www.youtube.com/embed/".concat(getVideoId(e.target.value));
});

function updatePoints() {
    document.getElementById("total-points").value = points;
    document.getElementById("total-busts").value = busts;
}

function startButton() {
    if(!nIntervId) {nIntervId = setInterval(displayTimer,10);}
    if(milliseconds > 0 && seconds < 35) {
        var pool = getPoolPoints();
        var currentPointFigure = pool[(pointAnalytics.length)%pool.length];
        currentTime = seconds + (milliseconds/1000);
        timeDiff = currentTime - lastTime;
        lastTime = currentTime;
        points++;
        pointAnalytics.push({
            "figure_uuid": currentPointFigure[0],
            "figure_text": currentPointFigure[1],
            "is_block": currentPointFigure[2],
            "points": points,
            "current_time": currentTime,
            "time_diff": timeDiff,
            "is_valid_point": true
        });
        if (pointAnalytics.length > 1
            && pointAnalytics.at(-1)['figure_uuid'] == pointAnalytics.at(-2)['figure_uuid']
            && !pointAnalytics.at(-2)['is_valid_point'])
            {points--;}
        registerPoint(pointAnalytics.length, currentTime, timeDiff, '✔');
        updatePoints();
    }
}

document.getElementById('start-button').addEventListener('click', startButton);

function bustButton() {
    if(seconds > 0 && seconds < 35) {
        busts++;
        var pool = getPoolPoints();
        var currentPointFigure = pool[(pointAnalytics.length)%pool.length];
        currentTime = seconds + (milliseconds/1000);
        timeDiff = currentTime - lastTime;
        lastTime = currentTime;
        pointAnalytics.push({
            "figure_uuid": currentPointFigure[0],
            "figure_text": currentPointFigure[1],
            "is_block": currentPointFigure[2],
            "points": points,
            "current_time": currentTime,
            "time_diff": timeDiff,
            "is_valid_point": false
        });
        if (pointAnalytics.length > 1
            && pointAnalytics.at(-1)['figure_uuid'] == pointAnalytics.at(-2)['figure_uuid']
            && pointAnalytics.at(-2)['is_valid_point'])
            {points--;}
        registerPoint(pointAnalytics.length, currentTime, timeDiff, '✘');
        updatePoints();
    }
}

document.getElementById('bust-button').addEventListener('click', bustButton);

function displayTimer(){
    milliseconds+=10;
    if(milliseconds == 1000){
        milliseconds = 0;
        seconds++;
        if(seconds == 35){
            clearInterval(nIntervId);
        }
    }

 let s = seconds < 10 ? "0" + seconds : seconds;
 let ms = milliseconds < 10 ? "00" + milliseconds : milliseconds < 100 ? "0" + milliseconds : milliseconds;

 timerRef.innerHTML = `${s} : ${ms}`;
}

function getPoolPoints() {
    const pool = [];
    for (let i = 1; i <= 5; i++) {
        var str = "pool-point";
        str += i;
        var point = document.getElementById(str);
        var pointValue = point.options[point.selectedIndex].value;
        var pointText = point.options[point.selectedIndex].text;
        if (pointText != "-") {
            if (blocks.includes(pointText)) {
                pool.push([pointValue, pointText.concat(' (start)'), true]);
                pool.push([pointValue, pointText.concat(' (end)'), true]);
            } else {
            pool.push([pointValue, pointText, false]);
            }
        }
    }
    return pool;
}

function createInput(name, value) {
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = name;
    input.value = value;
    return input;
}

function registerPoint(qty, currentTime, timeDiff, pointStatus) {
  var pool = getPoolPoints();
  var pointFigure = pool[(qty-1)%pool.length];
  var tbodyRef = document.getElementById("table-results").getElementsByTagName('tbody')[0];
  var newRow = tbodyRef.insertRow();
  var cell1 = newRow.insertCell();
  var cell2 = newRow.insertCell();
  var cell3 = newRow.insertCell();
  var cell4 = newRow.insertCell();
  var cell5 = newRow.insertCell();
  newRow.appendChild(createInput("point-number",(qty).toString()));
  newRow.appendChild(createInput("point-figure",pointFigure[0]));
  newRow.appendChild(createInput("current-time",currentTime.toFixed(2).toString()));
  newRow.appendChild(createInput("time-diff",timeDiff.toFixed(2).toString()));
  newRow.appendChild(createInput("point-status",pointStatus));
  cell1.appendChild(document.createTextNode((qty).toString()));
  cell2.appendChild(document.createTextNode(pointFigure[1]));
  cell3.appendChild(document.createTextNode(currentTime.toFixed(2).toString()));
  cell4.appendChild(document.createTextNode(timeDiff.toFixed(2).toString()));
  cell5.appendChild(document.createTextNode(pointStatus));
}

document.addEventListener('keydown', (event) => {
    if(event.key === 'q') {startButton();}
    if(event.key === 'w') {bustButton();}
});