import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import './Login.css'

class Login extends Component {
	render () {
		return (
			<div className="Login-page">
				<h1 className="Welcome-page">Welcome to Redraw!</h1> 
				<h2 className="Description">
					Making room draw a more enjoyable experience
				</h2>
				<Link to="/map">
					<Button />
				</Link>
			</div>
		);
	}
}

class Button extends Component {
	render () {
		return (
			<button className="Login-button"> Click Here to Login </button>
		);
	}
}
export default Login; 