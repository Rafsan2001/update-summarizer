function createInputBox(type, classNames, name, placeholder='') {
    const inputBox = document.createElement('input');
    inputBox.type = type;
    inputBox.name = name;
    inputBox.id = name;
    inputBox.className = classNames;
    inputBox.placeholder = placeholder || '';

    return inputBox;
}

window.onload = () => {
    const linkInputHolder = document.querySelector('.link-input-holder');
    const ild = document.getElementById('input-link-btn-decrease');
    const ils = document.getElementById('input-link-btn-show');
    const ili = document.getElementById('input-link-btn-increase');
    let fieldInputCount = 1;
    const fileCountHolder = document.querySelector('#file-count');
    const fileInputHolder = document.querySelector('.file-input-holder');
    const fld = document.getElementById('input-file-btn-decrease');
    const fls = document.getElementById('input-file-btn-show');
    const fli = document.getElementById('input-file-btn-increase');
    let fileFieldsCount = 1;

    const inputBox = createInputBox('text', 'form-control my-1', `link-input-1`, 'Enter your link here');
    linkInputHolder.appendChild(inputBox);

    const fileBox = createInputBox('file', 'form-control my-1', `file-input-1`);

    function generateLinkInputBox() {
        const inputBox = createInputBox('text', 'form-control my-1', `link-input-${fieldInputCount}`, 'Enter your link here');
        linkInputHolder.appendChild(inputBox);
    }

    function generateFileInputBox(holder, id) {
        const inputBox = createInputBox('file', 'form-control my-1', `file-input-${id}`);
        holder.appendChild(inputBox);
    }

    ild.addEventListener('click', () => {
        if (fieldInputCount !== 1) {
            fieldInputCount--;
            ils.innerText = fieldInputCount;
            linkInputHolder.removeChild(linkInputHolder.lastChild);

            if (fieldInputCount === 1) {
                ild.disabled = true;
            } else {
                ild.disabled = false;
            }
        }
    });

    ili.addEventListener('click', () => {
        fieldInputCount++;
        ils.innerText = fieldInputCount;
        generateLinkInputBox(linkInputHolder, fieldInputCount);

        if (fieldInputCount === 1) {
            ild.disabled = true;
        } else {
            ild.disabled = false;
        }
    });

    fld.addEventListener('click', () => {
        if (fileFieldsCount !== 1) {
            fileFieldsCount--;
            fls.innerText = fileFieldsCount;
            fileCountHolder.value = parseInt(fileFieldsCount);
            fileInputHolder.removeChild(fileInputHolder.lastChild);

            if (fileFieldsCount <= 1) {
                fld.disabled = true;
            } else {
                fld.disabled = false;
            }
        }
    });

    fli.addEventListener('click', () => {
        fileFieldsCount++;
        fls.innerText = fileFieldsCount;
        fileCountHolder.value = parseInt(fileFieldsCount);
        generateFileInputBox(fileInputHolder, fileFieldsCount);

        if (fileFieldsCount <= 1) {
            fld.disabled = true;
        } else {
            fld.disabled = false;
        }
    });

    const fileSubmitBtn = document.getElementById('file-submit');

    fileSubmitBtn.addEventListener('click', () => {
        const formData = new FormData();
        const inputFiles = document.querySelector('input[type="file"]')
        formData.append('num', fileFieldsCount);

        for (let i=1; i<=fileFieldsCount; i++) {
            formData.append(`file-input-${i}`, inputFiles.files[i]);
        }

        fetch('/summary-generate', {
            method: 'POST',
            body: formData,
        })
        .then((response) => console.log('Success'))
        .catch((error) => {
            console.error('Error:', error);
        });
    });    
}