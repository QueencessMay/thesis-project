const e1 = new EmojiPopover({
    button: '.toggle-emoji',
    container: 'html',
    targetElement: '.textarea-emoji',
    emojiList: [
        { value: '😀', },
        { value: '😄', },
        { value: '😁', },
        { value: '🤣', },
        { value: '😆', },
        { value: '😅', },
        { value: '🤣', },
        { value: '😂', },
        { value: '🙂', },
        { value: '😉', },
        { value: '😊', },
        { value: '😇', },
        { value: '🥰', },
        { value: '😍', },
        { value: '🤩', },
        { value: '😘', },
        { value: '😗', },
        { value: '😚', },
        { value: '😙', },
        { value: '🥲', },
        { value: '😏', },

        { value: '❤️', },
        { value: '💗', },
        { value: '💖', },
        { value: '💓', },
        { value: '💔', },
        { value: '❤️‍🩹', },
        { value: '💘', },
        { value: '❣️', },
        { value: '💙', },
        { value: '💚', },
        { value: '🖤', },
        { value: '💛', },
        { value: '💟', },
        { value: '🤍', },
        { value: '🤎', },
        { value: '💝', },
        { value: '🧡', },
        { value: '💜', },

        { value: '😕', },
        { value: '🫤', },
        { value: '😟', },
        { value: '🙁', },
        { value: '😮', },
        { value: '😟', },
        { value: '🙁', },
        { value: '😮', },
        { value: '😯', },
        { value: '😲', },
        { value: '😳', },
        { value: '🥺', },
        { value: '🥹', },
        { value: '😦', },
        { value: '😨', },
        { value: '😰', },
        { value: '😥', },
        { value: '😢', },
        { value: '😭', },
        { value: '😱', },
        { value: '😖', },
        { value: '😣', },
        { value: '😞', },
        { value: '😓', },
        { value: '😩', },
        { value: '😫', },
        { value: '😖', },
        { value: '😤', },
        { value: '😠', },
        { value: '😡', },
        { value: '🤬', },
        { value: '👿', },

        { value: '🙃', },
        { value: '🫠', },
        { value: '🤐', },
        { value: '🤨', },
        { value: '😐', },
        { value: '😑', },
        { value: '😶', },
        { value: '🫥', },
        { value: '😶‍🌫️', },
        { value: '😒', },
        { value: '🙄', },
        { value: '😬', },
        { value: '😮‍💨', },
        { value: '🤥', },
        { value: '🫨', },
    ]
})

const textarea = document.querySelector(".textarea-emoji");

textarea.addEventListener("focus", (event) => {
    event.preventDefault();
});

e1.onSelect(val => {
    const cursorPosition = textarea.selectionStart;
    const valToInsert = val;
    const currentValue = textarea.value;
    const updatedValue =
        currentValue.slice(0, cursorPosition) +
        valToInsert +
        currentValue.slice(cursorPosition);
    textarea.value = updatedValue;
    const newCursorPosition = cursorPosition + valToInsert.length;
    textarea.setSelectionRange(newCursorPosition, newCursorPosition);
});