let bocaAberta = false;
let aguardandoResposta = false;
let verificacaoConcluida = false;

const elementoVideo = document.getElementById('video');
const elementoCanvas = document.getElementById('saida');
const elementoInstrucoes = document.getElementById('instrucoes');
const contextoCanvas = elementoCanvas.getContext('2d');

const faceMesh = new FaceMesh({locateFile: (arquivo) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${arquivo}`});

faceMesh.setOptions({
    maxNumFaces: 1,
    refineLandmarks: true,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5,
});

faceMesh.onResults((results) => {
    contextoCanvas.save();
    contextoCanvas.clearRect(0, 0, elementoCanvas.width, elementoCanvas.height);
    contextoCanvas.drawImage(results.image, 0, 0, elementoCanvas.width, elementoCanvas.height);

    if (results.multiFaceLandmarks.length > 0) {
        const landmarks = results.multiFaceLandmarks[0];

        if (!aguardandoResposta && bocaEstaAberta(landmarks)) {
            bocaAberta = true;
            aguardandoResposta = true;
            elementoInstrucoes.innerText = 'Verificando...';
            enviaImagem(results.image);
        }

        if (!verificacaoConcluida && !aguardandoResposta) {
            aguardandoResposta = true;
            setTimeout(() => {
                if (!verificacaoConcluida) {
                    bocaAberta = false;
                    elementoInstrucoes.innerText = 'Abra a boca';
                    aguardandoResposta = false;
                }
            }, 5000);
        }
    }
    contextoCanvas.restore();
});

const camera = new Camera(elementoVideo, {
    onFrame: async () => {
        await faceMesh.send({image: elementoVideo});
    },
    width: 640,
    height: 480,
});
camera.start();

function bocaEstaAberta(landmarks) {
    const top = landmarks[13];
    const bottom = landmarks[14];
    const distancia = Math.abs(top.y - bottom.y);
    return distancia > 0.03;
}

function enviaImagem(elementoImagem) {
    const canvas = document.createElement('canvas');
    canvas.width = elementoImagem.width;
    canvas.height = elementoImagem.height;
    const contexto = canvas.getContext('2d');
    contexto.drawImage(elementoImagem, 0, 0, canvas.width, canvas.height);
    const imagemData = canvas.toDataURL('image/jpeg');

    fetch('/usuario/reconhecimento-facial/reconhecimento/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({imagem: imagemData})
    })
    .then(response => response.json())
    .then(data => {
        if (data.vivacidade && !data.fraude && !data.reflexo && !data.textura && !data.bordas_artificiais) {
            elementoInstrucoes.innerText = 'Verificação concluída com sucesso!';
            aguardandoResposta = true;
            bocaAberta = true;
            verificacaoConcluida = true;

            elementoVideo.style.display = 'none';
            elementoCanvas.style.display = 'none';

            setTimeout(() => {
                window.location.href = '/'; // enviar do back
            }, 3000);
        } else {
            elementoInstrucoes.innerText = 'Verificação falhou. Tente novamente.';

            setTimeout(() => {
                bocaAberta = false;
                aguardandoResposta = false;
                elementoInstrucoes.innerText = 'Abra a boca';
            }, 3000);
        }
    })
    .catch(error => {
        elementoInstrucoes.innerText = 'Erro na verificação. Tente novamente.';

        setTimeout(() => {
            bocaAberta = false;
            aguardandoResposta = false;
            elementoInstrucoes.innerText = 'Abra a boca';
        }, 3000);
    })
}