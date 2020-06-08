import React from 'react'
import Plotly from 'plotly.js-basic-dist'
import createPlotlyComponent from 'react-plotly.js/factory'
import Configuration from '../config'

class SessionComponent extends React.Component{
  constructor(props){
    super(props);

    this.state = {
      sessionItems: null,
      selectedSession: null,
    };

    this.emptyOption = [(<option selected disabled hidden value=''></option>)];

    this.buildSessionOptions = this.buildSessionOptions.bind(this);
    this.onSessionSelect = this.onSessionSelect.bind(this);
    this.buildSessionFileOptions = this.buildSessionFileOptions.bind(this);
    this.onFileSelect = this.onFileSelect.bind(this);
    this.createPlotsDiv = this.createPlotsDiv.bind(this);
  }

  componentDidMount(){
    fetch(Configuration.app_url + 'session')
      .then(res => res.json())
      .then((result) =>{
        this.setState({
          sessionItems: result.sessions,
        })
      });
  }

  buildSessionOptions(){
    if(this.state.sessionItems){
      return this.emptyOption.concat(this.state.sessionItems.map((sessionItem) => {
        return (
          <option value={sessionItem.id}>
            {sessionItem.name}
          </option>
        )
      }));
    }
    else{
      return null;
    }
  }

  buildSessionFileOptions(){
    if(this.state.selectedSessionFiles){
      return this.emptyOption.concat(this.state.selectedSessionFiles.map((sessionFile)=>{
        return (
          <option value={sessionFile.id}>
            {sessionFile.name}
          </option>
        )
      }));
    }
  }

  onSessionSelect(event){
    let sessionId = event.target.value;
    fetch(Configuration.app_url + 'session/' + sessionId + "/file")
      .then(res => res.json())
      .then((result) =>{
        this.setState({
          selectedSession: sessionId,
          selectedSessionFiles: result.files,
        });
      });
  }

  onFileSelect(event){
    let fileId = event.target.value;
    fetch(Configuration.app_url + 'session/' + this.state.selectedSession + "/file/" + fileId)
      .then(res => res.json())
      .then((result) =>{
        this.setState({
          selectedFile: fileId,
          selectedFileIterations: this.parseIterations(result.iterations)
        });
      });
  }
  
  parseIterations(iterations){
    let iteration_labels = [];
    let iteration_contents = [];
    let iteration_vars = {};

    iterations.forEach((iteration) => {
      iteration_labels.push(iteration.label);
      iteration_contents.push(iteration_contents);

      Object.keys(iteration.var).forEach((key) => {
        if(!Object.keys(iteration_vars).includes(key)){
          iteration_vars[key] = [];
        }
        iteration_vars[key].push(iteration.var[key]);
      });
    });

    return {
      labels: iteration_labels,
      contents: iteration_contents,
      vars: iteration_vars,
    };
  }

  createPlotsDiv(data, layout){
    let plot_datas = []
    Object.keys(this.state.selectedFileIterations.vars).forEach((key) =>{
      let vals = this.state.selectedFileIterations.vars[key];
      let data = {
        x: [...Array(vals.length)].keys(),
        y: vals,
        type: 'scatter',
        mode: 'lines+markers',
        name: key,
      };

      plot_datas.push(data);
    });

    let plot = createPlotlyComponent(Plotly);
    let plot_el = React.createElement(plot, {
      data: plot_datas,
      layout: {
        width: 800, 
        height: 600, 
        xaxis: {
          title: 'iteration',
        },
        yaxis: {
          title: 'fitness',
        }
      }
    });

    return (
      <div>
        {plot_el}
      </div>
    );
  }

  render(){
    let sessionSelect = (
      <div>
        <label>Session: </label> 
        <select name="session_select" id="session_select" onChange={this.onSessionSelect}>
          {this.buildSessionOptions()}
        </select>
      </div>
    );

    let sessionFileSelect = null;
    if(this.state.selectedSession){
      sessionFileSelect = (
        <div>
          <label>File: </label>
          <select name="file_select" id="file_select" onChange={this.onFileSelect}>
            {this.buildSessionFileOptions()}
          </select>
        </div>
      )
    }

    let sessionDisplay = null;
    if(this.state.selectedFile){
      sessionDisplay = (
        <div>
          {this.createPlotsDiv()}
        </div>
      );
    }

    return (
      <div>
        {sessionSelect}
        {sessionFileSelect}
        {sessionDisplay}
      </div>
    );
  }
}

export default SessionComponent