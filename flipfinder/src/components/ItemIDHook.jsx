import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import GetItem from './GetItem';
function ItemIDHook() {
  return <GetItem id={useParams()}></GetItem>;
}

export default ItemIDHook;
