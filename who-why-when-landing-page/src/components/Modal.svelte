<script>
    import { createEventDispatcher } from 'svelte';

    export let onClose;

    const dispatch = createEventDispatcher();

    function close() {
        dispatch('close');
        if (onClose) onClose();
    }
</script>

<div class="modal">
    <div class="modal-content">
        <button class="close-btn" on:click={close}>&times;</button>
        <slot></slot>
    </div>
</div>

<style>
    .modal {
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1000;
    }

    .modal-content {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        width: 100%;
        position: relative;
    }

    .close-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
    }
</style>
