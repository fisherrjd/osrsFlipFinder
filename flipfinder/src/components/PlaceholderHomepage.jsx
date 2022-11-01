import React, {Component} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

class PlaceholderHome extends Component {
  constructor(props) {
    super(props);
    this.state = {items: []};
  }
  componentDidMount() {
    axios.get(`http://${window.location.host}/api/margin`).then((response) => {
      this.setState({items: response.data.items});
      console.log(this.state.items);
    });
  }
  render() {
    const {items} = this.state;
    return (
      <div>
        {items.map((item) => (
          <Accordion key={item.id}>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1a-content"
              id="panel1a-header"
            >
              <p>{item.name}</p>
            </AccordionSummary>
          </Accordion>
        ))}
      </div>
    );
  }
}

export default PlaceholderHome;
