document.addEventListener('DOMContentLoaded', () => {
    const checkButton = setInterval(() => {
        const button = document.getElementById('readme-button');
        if (button) {
            console.log('Readme button found, triggering click...');
            button.click();
            clearInterval(checkButton); // �����ˬd
        }
    }, 100); // �C 100 �@���ˬd�@��
});