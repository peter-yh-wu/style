import React from 'react';
import RaisedButton from '@material-ui/core/Button';
import {TextField} from '@material-ui/core';

// https://stackoverflow.com/questions/38154469/form-with-material-ui
class IOForm extends React.Component {
  constructor() {
    super();
    this.state = {
      input_value: null,
      output_value: null,
    };
  }

  handleInputChange = (event) => {
    this.setState({input_value: event.target.value});
  }

  handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('input', this.state.input_value);
    let result = await fetch('http://34.82.174.216:5000/trump', {
      method: 'POST',
      body: formData
    }).then(response => response.json())
    .catch(
      (error) => {
        alert(error);
      }
    )

    this.setState({output_value: result.output});
    document.getElementById("output").innerHTML = this.state.output_value;
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <TextField floatingLabelText="ID Number" onChange={this.handleInputChange} />
          <RaisedButton label="Submit" type="submit" border-color="black">Trumpify</RaisedButton>
        </form>

      <p id="output" />
      </div>
    )
  }
}

export default IOForm;
