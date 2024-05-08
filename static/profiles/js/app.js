class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState());

        sendButton.addEventListener('click', () => this.onSendButton());


        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton();
            }
        });
    }

    toggleState() {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            this.args.chatBox.classList.add('chatbox--active');
        } else {
            this.args.chatBox.classList.remove('chatbox--active');
        }
    }

    onSendButton() {
        var textField = this.args.chatBox.querySelector('input');
        let text1 = textField.value;
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 };
        this.messages.push(msg1);

        fetch($SCRIPT_ROOT +'/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "AgronomoBot", message: r.Answer };
            this.messages.push(msg2);
            this.updateChatText();

            textField.value = '';
        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText();
            textField.value = '';
          });
    }

    updateChatText() {
        var html = '';
        this.messages.slice().reverse().forEach(item => {
            if (item.name === "AgronomoBot") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatmessage = this.args.chatBox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();
