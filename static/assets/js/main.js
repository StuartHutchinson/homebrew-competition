(function() {
  "use strict";

  /*
  Toggle the navbar
  */
  const headerToggleBtn = document.querySelector('.header-toggle');
  function headerToggle() {
    document.querySelector('#header').classList.toggle('header-show');
    this.classList.toggle('bi-list');
    this.classList.toggle('bi-x');
  }
  headerToggleBtn.addEventListener('click', headerToggle);

  /*
  Add a new purchase, or cancel the adding
  */
  const addPurchaseBtn = document.querySelector('.add-purchase');
  function togglePurchaseForm() {
        var purchaseForm = document.getElementById('purchase-form');
        /*purchaseForm.style.display = 'block';*/
        purchaseForm.classList.toggle('d-block');
        purchaseForm.classList.toggle('d-none');
        this.innerText = this.innerText === "Add Purchase" ? "Cancel" : "Add Purchase";
  }
  addPurchaseBtn.addEventListener('click', togglePurchaseForm);


  })();