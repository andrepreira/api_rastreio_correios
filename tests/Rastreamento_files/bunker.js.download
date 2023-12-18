import './menu.js';
import './botoes.js';
import './acessibilidade.js';
import * as forms from './forms.js';
import * as modal from './modal.js';
import * as alerta from './alerta.js';
import * as tabs from './tabs.js';
import * as tabelas from './tabelas.js';

document.body.classList.remove('oculto');
// Tema escuro da Black Friday
//document.body.classList.add('contrast');

if ('ontouchstart' in window) {
  document.body.classList.add('touch');
}

if (!document.querySelector('body > footer')) {
  document.body.classList.add('modo-foco');
}

const loading = document.getElementById('loading');

const loadingVisivel = ev => {
  loading.classList.add('visivel');
  setTimeout(() => {
    loading.classList.remove('visivel');
  }, 30000);
};

const registraLoading = () => {
  document.querySelectorAll('a[href]:not([target="_blank"])').forEach(a => {
    a.addEventListener('click', loadingVisivel);
  });
};

const observa = () => {
  observer.observe(document.body, { attributes: true, childList: true, subtree: true });
};

const observer = new MutationObserver(() => {
  registraLoading();
});
observa();
registraLoading();

export { forms, modal, alerta, tabs };