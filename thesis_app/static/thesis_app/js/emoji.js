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
        { value: '❤️‍🔥', },
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

        { value: '🫶', },
        { value: '👎', },
        { value: '👍', },
        { value: '👌', },
        { value: '✌️', },
        { value: '✍️', },
        { value: '👋', },
        { value: '✋', },

        { value: '💀', },
        { value: '🔥', },
        { value: '✨', },
        { value: '⭐', },
        { value: '✔️', },
        { value: '✅', },
        { value: '🎉', },
        { value: '👀', },
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
        { value: '🤔', },
        { value: '🫨', },
        { value: '🫠', },
    ]
})

const textarea = document.querySelector(".textarea-emoji");

e1.onSelect(val => {
    const cursorPosition = textarea.selectionStart;
    const valToInsert = val;
    const currentValue = textarea.value;

    const emojiPosition = cursorPosition;
    const updatedValue =
        currentValue.slice(0, emojiPosition) +
        valToInsert +
        currentValue.slice(emojiPosition);

    textarea.value = updatedValue;
    const newCursorPosition = emojiPosition + valToInsert.length;
    textarea.setSelectionRange(newCursorPosition, newCursorPosition);
    textarea.focus();
});



