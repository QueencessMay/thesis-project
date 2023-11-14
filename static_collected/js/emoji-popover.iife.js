var EmojiPopover = (function () {
  "use strict";
  return class {
    constructor(t) {
      this.opts = t;
      (this.options = Object.assign(
        {},
        {
          container: "body",
          button: ".e-btn",
          targetElement: ".e-input",
          emojiList: [],
          wrapClassName: "",
          wrapAnimationClassName: "anim-scale-in",
        },
        t
      )),
        (this.wrapClassName = "emoji-wrap"),
        (this.wrapCount = document.querySelectorAll(".emoji-wrap").length + 1),
        (this.wrapCountClassName = `emoji-wrap-${this.wrapCount}`),
        this.init(),
        this.createButtonListener();
    }
    init() {
      const {
          emojiList: t,
          container: e,
          button: s,
          targetElement: i,
        } = this.options,
        a = this.createEmojiContainer(),
        n = this.createEmojiList(t),
        o = this.createMask();
      a.appendChild(n), a.appendChild(o);
      const r = document.querySelector(i),
        { left: c, top: l, height: m } = r.getClientRects()[0];
      (a.style.top = `${l + m + 10}px`), (a.style.left = `${c}px`);
      document.querySelector(e).appendChild(a);
    }
    createButtonListener() {
      const { button: t } = this.options;
      document
        .querySelector(t)
        .addEventListener("click", () => this.toggle(!0));
    }
    createEmojiContainer() {
      const { wrapAnimationClassName: t, wrapClassName: e } = this.options,
        s = document.createElement("div");
      return (
        s.classList.add(this.wrapClassName),
        s.classList.add(this.wrapCountClassName),
        s.classList.add(t),
        "" !== e && s.classList.add(e),
        s
      );
    }
    createEmojiList(t) {
      const e = document.createElement("div");
      return (
        e.classList.add("emoji-list"),
        t.forEach((t) => {
          const s = this.createEmojiItem(t);
          e.appendChild(s);
        }),
        e
      );
    }
    createEmojiItem(t) {
      const { value: e, label: s } = t,
        i = document.createElement("div");
      let a;
      var n;
      return (
        (n = e),
        new RegExp("http").test(n)
          ? ((a = document.createElement("img")),
            a.classList.add("emoji"),
            a.classList.add("emoji-img"),
            a.setAttribute("src", e))
          : ((a = document.createElement("span")),
            a.classList.add("emoji"),
            a.classList.add("emoji-text"),
            (a.innerText = e)),
        i.classList.add("emoji-item"),
        i.appendChild(a),
        "string" == typeof s && i.setAttribute("title", s),
        i
      );
    }
    createMask() {
      const t = document.createElement("div");
      return (
        t.classList.add("emoji-mask"),
        t.addEventListener("click", () => this.toggle(!1)),
        t
      );
    }
    toggle(t) {
      document.querySelector(`.${this.wrapCountClassName}`).style.display = t
        ? "block"
        : "none";
    }
    onSelect(t) {
      const e = document.querySelectorAll(
          `.${this.wrapCountClassName} .emoji-item`
        ),
        s = this;
      e.forEach(function (e) {
        e.addEventListener("click", function (e) {
          const i = e.currentTarget;
          let a;
          (a = i.children[0].classList.contains("emoji-img")
            ? i.children[0].getAttribute("src")
            : i.innerText),
            s.toggle(!1),
            t(a);
        });
      });
    }
  };
})();
