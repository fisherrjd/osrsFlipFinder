import React, {Component} from 'react';
import {Link} from 'react-router-dom';
class PlaceholderHome extends Component {
  render() {
    const placeholderItems = [
      {name: 'Abyssal Whip', id: 4151},
      {name: 'Helm of Neitiznot', id: 10828},
      {name: 'Granite Maul', id: 4153},
      {name: 'Dragon Scimitar', id: 4587},
      {name: 'Armadyl Godsword', id: 11802},
    ];
    return placeholderItems.map((item) => (
      <Link to={`/itemdetails/${item.id}`}>
        <div>
          <button key={item.id}>{item.name}</button>
        </div>
      </Link>
    ));
  }
}

export default PlaceholderHome;
