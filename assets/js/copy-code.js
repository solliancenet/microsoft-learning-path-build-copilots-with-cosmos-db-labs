document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('pre > code').forEach((codeBlock) => {
      const button = document.createElement('button');
      button.className = 'copy-code-button';
      button.type = 'button';
      button.innerText = 'Copy';
  
      button.addEventListener('click', () => {
        const code = codeBlock.innerText;
  
        navigator.clipboard.writeText(code).then(
          () => {
            button.innerText = 'Copied!';
            setTimeout(() => (button.innerText = 'Copy'), 2000);
          },
          (err) => {
            console.error('Failed to copy: ', err);
            button.innerText = 'Error';
          }
        );
      });
  
      const pre = codeBlock.parentNode;
      pre.style.position = 'relative';
      pre.appendChild(button);
    });
  });
  