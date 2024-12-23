document.addEventListener('DOMContentLoaded', () => {
    const checkButton = setInterval(() => {
        const button = document.getElementById('readme-button');
        if (button) {
            console.log('Readme button found, triggering click...');
            button.click();
            clearInterval(checkButton); // 停止檢查
        }
    }, 100); // 每 100 毫秒檢查一次
});