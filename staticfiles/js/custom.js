const burger = document.getElementById('burger');
    const dropdown = document.querySelector('.dropdown');

    burger.addEventListener('change', () => {
      if (burger.checked) {
        dropdown.classList.add('slide-down');
        dropdown.classList.remove('slide-up');
        dropdown.style.display = 'block';
      } else {
        dropdown.classList.add('slide-up');
        dropdown.classList.remove('slide-down');
      }
    });

    dropdown.addEventListener('animationend', (event) => {
      if (event.animationName === 'slideUp') {
        dropdown.style.display = 'none';
      }
    });