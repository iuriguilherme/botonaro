/*
 *  Botonaro  
 * Copyright 2022-2023 Iuri Guilherme <https://iuri.neocities.org/>  
 * Creative Commons 4.0 Attribution Share Alike  
*/

// https://getbootstrap.com/docs/5.2/components/modal/
const imageModal = document.getElementById('imageModal')
imageModal.addEventListener('show.bs.modal', event => {
    const trigger = event.relatedTarget
    const image = trigger.getAttribute('src')
    const modalImage = imageModal.querySelector('.modal-body img')
    modalImage.src = `${image}`
})
