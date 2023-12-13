document.addEventListener('DOMContentLoaded', () => {
  const message = document.querySelector('.message');
  message.addEventListener('mouseover', () => {
    message.style.color = 'red';
  });
  message.addEventListener('mouseout', () => {
    message.style.color = 'black';
  });
});
