import React from 'react';
import './App.css';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import {TextField} from '@material-ui/core';
//import React, { Component } from 'react'
//import NavBar from './components/NavBar'

import IOForm from './components/ioform'

function App() {
  return (
    <div className="body">
    <div className="Title">
    <h1> Tweet2Transfer   </h1>
    <img src= {require("/Users/lawrenceli/Documents/cs/hacklodge/style/flask-react/src/TRUMP.png")} width="200px" />
    </div>
    <div className="Forms">
      <IOForm />
    </div>
    </div>

      //<TextField hintText="Hint" name="Name" fullWidth={true} />


      //<TextField
       // id="first-name"
        //label="Name"
        //value={this.state.name}
        //onChange={this.handleChange('name')}
        //margin="normal"
    ///>
      //< Button variant = "contained" color = "primary">

  );
}


export default App;
