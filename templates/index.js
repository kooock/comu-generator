let cos = []
let mus = []

let co = document.getElementById("co");
let mu = document.getElementById("mu");
let describeContainers = document.getElementsByClassName("describe-container")
let coWord = document.getElementById("co-word");
let muWord = document.getElementById("mu-word");
let coDesc = document.getElementById("co-desc");
let muDesc = document.getElementById("mu-desc");
let coPostposition = document.getElementById("co-postposition")
let animated = false;
let indexCo = 0;
let indexMu = 0;
let cachedCo = 0;
let cachedMu = 0;
let lenCo = 0;
let lenMu = 0;
let lastCo = "";
let genButton = document.getElementById("gen-btn");

const shuffle = (array) => array.sort(() => Math.random() - 0.5);

const animateText = () => {
    if (animated) {
        co.classList.add("text-out")
        mu.classList.add("text-out")
        co.classList.remove("text-in")
        mu.classList.remove("text-in")
        setTimeout(function () {
            co.innerText = cos[indexCo]["word"];
            mu.innerText = mus[indexMu]["word"];
            coWord.innerText = "코" + cos[indexCo]["word"];
            muWord.innerText = "무" + mus[indexMu]["word"];
            coDesc.innerText = cos[indexCo]["desc"];
​            muDesc.innerText = mus[indexMu]["desc"];
            lastCo = cos[indexCo]["word"].charAt(cos[indexCo]["word"].length-1)
​            if ((lastCo.charCodeAt() - "가".charCodeAt()) % 28 == 0 ){
​                coPostposition.innerText = "랑"
​            } else {
​                coPostposition.innerText = "이랑"
​            }
            co.classList.add("text-in")
            mu.classList.add("text-in")
            co.classList.remove("text-out")
            mu.classList.remove("text-out")
            cachedCo = indexCo;
            cachedMu = indexMu;
            if (indexCo == lenCo - 1) {
                indexCo = 0;
            } else {
                indexCo++;
            }

            if (indexMu == lenMu - 1) {
                indexMu = 0;
            } else {
                indexMu++;
            }
        }, 140)
    }
    setTimeout(animateText,160);
}

fetch('/cos')
    .then(function(response) {
        return response.json();
    })
    .then(function(myJson) {
        lenCo = myJson.length
        cos = shuffle(myJson);
        animated = true;
        animateText();
    });

fetch('/mus')
    .then(function(response) {
        return response.json();
    })
    .then(function(myJson) {
        mus = shuffle(myJson);
    });



const onClick = () => {
    if (animated) {
        animated = false
        for (let i = 0; i < describeContainers.length; i++) {
            describeContainers[i].style.display = "block"
        }
    } else {
        animated = true;
        for (let i = 0; i < describeContainers.length; i++) {
            describeContainers[i].style.display = "none"
        }
        setTimeout(()=> {
            animated = false;
            for (let i = 0; i < describeContainers.length; i++) {
                describeContainers[i].style.display = "block"
            }
        }, 5000)
    }
}

genButton.addEventListener("click",onClick)