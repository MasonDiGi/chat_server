// Import required components and functions
import React from 'react';
import axios from "axios";
import {Button, Form, Jumbotron, InputGroup, FormControl} from "react-bootstrap";
import {API_URL} from "./urls";

class ComboPage extends React.Component {
    // Initalize the component with all the variables and functions used
    constructor(props) {
        super(props);
        // Attributes
        this.state = {
            loggedIn: false,
            name: "",
            index: null,
            messages: {},
            messageToSend: "",
        }
        // Methods that I created
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.scrollToBottom = this.scrollToBottom.bind(this);
        this.messageSent = this.messageSent.bind(this);
        this.handleKeyPress = this.handleKeyPress.bind(this);
        // References to tags in the script so I can edit them from js
        this.el = React.createRef();
        this.cont = React.createRef();
        this.msgInput = React.createRef();
    }

    // When the login form is sumbitted, call this
    handleSubmit(e) {
        e.preventDefault();
        // Create the data to POST to API
        let formData = new FormData();
        formData.append("name", this.state.name);
        // Send request to API and when it responds save the user's index into the state and toggle loggedIn
        axios.post(`http://${API_URL}/login`, formData).then(r => {
            this.setState({index: r.data});
            this.setState({loggedIn: true});
            this.scrollToBottom();
        });
    }

    // When either the message or login form is updated, update the state as well
    handleChange(e) {
        e.preventDefault();
        this.setState({[e.target.id]: e.target.value});
    }

    // When this component first spawns in, set listeners and timers to get messages and handle logging out if the
    // tab gets closed suddenly
    componentDidMount() {
        // Periodically get messages
        this.interval = setInterval(() => {
            axios.get(`http://${API_URL}/getmessages`).then(r => {
                if (this.state.messages && this.el.current) {
                    if (Math.round(this.el.current.getBoundingClientRect().bottom) === Math.round(this.cont.current.getBoundingClientRect().bottom)) {
                        this.setState({messages: r.data});
                        this.scrollToBottom();
                    } else {
                        this.setState({messages: r.data});
                    }
                } else {
                    this.setState({messages: r.data});
                }
            });
        }, 1000);
        // Call this if the tab is closed so the user can log out
        window.addEventListener("beforeunload", (e) => {
            if (this.state.index == null) {
                window.close();
            }
            let formData = new FormData();
            formData.append("id", this.state.index);
            axios.post(`http://${API_URL}/logout`, formData).then(r => {
                window.close();
            });
        });
    }

    // A callable function to scroll the page to the bottom with the newest message when needed
    scrollToBottom() {
        if (this.el.current) {
            this.el.current.scrollIntoView({behavior: "smooth"});
        }
    }

    // Called when the sumbit is pressed on the sendmessage field
    messageSent() {
        // Sends POST request to API and scrolls to the bottom of the page and clear the input field
        let formData = new FormData();
        formData.append("id", this.state.index);
        formData.append("msg", this.state.messageToSend);
        axios.post(`http://${API_URL}/sendmessage`, formData).then(r => {
            this.scrollToBottom();
            this.msgInput.current.value = "";
        });
    }

    // Send a message when ENTER is pressed as well
    handleKeyPress(e) {
        if (e.key === "Enter") {
            this.messageSent();
        }
    }

    // The HTML of the acutal component
    render() {
        // The login form
        if (!this.state.loggedIn) {
            return (
                <Jumbotron className={"m-5"}>
                    <Form onSubmit={this.handleSubmit}>
                        <Form.Group controlId="name">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" placeholder="Enter username" onChange={this.handleChange}/>
                            <Form.Text className="text-muted">
                                This will be temporary and nothing will be saved.
                            </Form.Text>
                        </Form.Group>
                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form>
                </Jumbotron>
            );
        // The message page
        } else {
            return (
                <Jumbotron id="messageDisplay" className="m-5">
                    {/* Basically a for loop to show all the messages */}
                    <div id="messages" ref={this.cont}>
                        {this.state.messages.map((val, id) => {
                            return (
                                <div key={id}>
                                    {val} <br/>
                                </div>
                            );
                        })}
                        <div ref={this.el} />
                    </div>
                    {/* The form for sending new messages */}
                    <InputGroup className="mb-3">
                        {/* Prepends the name before the prompt */}
                        <InputGroup.Prepend>
                            <InputGroup.Text id="messageInput">
                                [{this.state.name}]:
                            </InputGroup.Text>
                        </InputGroup.Prepend>
                        {/* The actual prompt, set to update the state, send message when needed, and handle enter being pressed */}
                        <FormControl onKeyPress={this.handleKeyPress} onChange={this.handleChange} id="messageToSend" ref={this.msgInput} aria-describedby="messageInput" />
                        <InputGroup.Append>
                            {/* Submit button to call the send function */}
                            <Button variant="outline-dark" onClick={this.messageSent}>Send</Button>
                        </InputGroup.Append>
                    </InputGroup>
                </Jumbotron>
            );
        }
    }
}

export default ComboPage;