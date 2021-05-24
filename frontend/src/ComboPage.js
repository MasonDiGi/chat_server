import React from 'react';
import axios from "axios";
import {Button, Form, Jumbotron, InputGroup, FormControl} from "react-bootstrap";
import {API_URL} from "./urls";

class ComboPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loggedIn: false,
            name: "",
            index: null,
            messages: {},
            messageToSend: "",
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.scrollToBottom = this.scrollToBottom.bind(this);
        this.messageSent = this.messageSent.bind(this);
        this.el = React.createRef();
        this.cont = React.createRef();
    }

    handleSubmit(e) {
        e.preventDefault();
        let formData = new FormData();
        formData.append("name", this.state.name);
        axios.post(`http://${API_URL}/login`, formData).then(r => {
            this.setState({index: r.data});
            this.setState({loggedIn: true});
            this.scrollToBottom();
        });
    }

    handleChange(e) {
        e.preventDefault();
        this.setState({[e.target.id]: e.target.value});
    }

    componentDidMount() {
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

    componentWillUnmount() {
    }

    scrollToBottom() {
        if (this.el) {
            this.el.current.scrollIntoView({behavior: "smooth"});
        }
    }

    messageSent(e) {
        e.preventDefault();
        let formData = new FormData();
        formData.append("id", this.state.index);
        formData.append("msg", this.state.messageToSend);
        axios.post(`http://${API_URL}/sendmessage`, formData).then(r => {
            this.scrollToBottom();
        });
    }

    render() {
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
        } else {
            return (
                <Jumbotron id="messageDisplay" className="m-5">
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
                    <InputGroup className="mb-3">
                        <InputGroup.Prepend>
                            <InputGroup.Text id="messageInput">
                                [{this.state.name}]:
                            </InputGroup.Text>
                        </InputGroup.Prepend>
                        <FormControl onChange={this.handleChange} id="messageToSend" aria-describedby="messageInput" />
                        <InputGroup.Append>
                            <Button variant="outline-dark" onClick={this.messageSent}>Send</Button>
                        </InputGroup.Append>
                    </InputGroup>
                </Jumbotron>
            );
        }
    }
}

export default ComboPage;