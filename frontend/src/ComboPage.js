import React from 'react';
import axios from "axios";
import {Button, Form, Jumbotron} from "react-bootstrap";
import {API_URL} from "./urls";

class ComboPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loggedIn: false,
            name: "",
            index: null,
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleSubmit(e) {
        e.preventDefault();
        let formData = new FormData();
        formData.append("name", this.state.name);
        axios.post(`http://${API_URL}/login`, formData).then(r => {
            this.setState({index: r.data});
            console.log(this.state);
        })
    }

    handleChange(e) {
        e.preventDefault();
        this.setState({name: e.target.value});
    }

    componentDidMount() {
        window.addEventListener("beforeunload", (e) => {
            let formData = new FormData();
            formData.append("id", this.state.index);
            axios.post(`http://${API_URL}/logout`, formData).then(r => {
                window.close();
            });
        });
    }

    componentWillUnmount() {
    }

    render() {
        return (
            <Jumbotron className={"m-5"}>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Group controlId="username">
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text" placeholder="Enter username" onChange={this.handleChange} />
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
    }
}

export default ComboPage;