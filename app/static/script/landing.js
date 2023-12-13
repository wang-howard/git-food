document.addEventListener('DOMContentLoaded', function () {

  // Smooth scroll for navigation links
  const links = document.querySelectorAll("nav a");
  for (const link of links) {
    link.addEventListener('click', function (event) {
      event.preventDefault();
      const targetId = this.getAttribute('href');
      const targetSection = document.querySelector(targetId);
      targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  // Dynamic hover effect on 'Get Started' button
  const getStartedButton = document.querySelector('.btn');
  getStartedButton.addEventListener('mouseover', function () {
    this.style.backgroundColor = '#333';
    this.style.color = '#e8491d';
  });

  getStartedButton.addEventListener('mouseout', function () {
    this.style.backgroundColor = '';
    this.style.color = '';
  });

});
