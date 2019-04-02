


import React from 'react';
import { ListItem, Dimensions, TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import { Col, Row, Grid } from "react-native-easy-grid";
import Icon from 'react-native-vector-icons/AntDesign'
import IconMaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons'
import PinchZoomView from 'react-native-pinch-zoom-view';


import { Svg } from 'expo';
const { Circle, Rect, Path, Line, Text, G, Defs, Use } = Svg;

/* Icon used from here for back button, this might be taken away */
// https://oblador.github.io/react-native-vector-icons/

var NoteSVG = require('./jsons/NotesData.json');
var MiscJson = require('./jsons/EditMisc.json');


/* getting the dims of the screen that is accessing this code */
const SCREEN_WIDTH = Dimensions.get('window').width
const SCREEN_HEIGHT = Dimensions.get('window').height

/* this is the total amount of beats in the music sheet currently */
var totalBeats = 0;

/* Setting a varible for the screen_height that can be modified */
var screenSize = SCREEN_HEIGHT;
/* how far to make the screen go down */
var screenExtendSize = 0;

var CleffLines;

var troubleCleffSplit = [];
var baseCleffSplit = [];
var altoCleffSplit = [];

var keyvalue;

var firstRender = 1;

/* This is the sheet id to update */
var sheet_id;

var forceRender = true;

/*
 * This is the Component that holds all the notes and
 * renders each note depending on the note num, pitch, and length
 */

export default class NoteObjects extends React.Component {

  /**
   * This sets up the state and the functions to
   * change the state
   */
  constructor(props) {
    super(props);
    // console.log("Props:");
    // console.log(this.props);

    /* Sets up the state with note num, pitch, Location, and color */
    this.state = {
      note: this.props.note,
      color: this.props.color,
      x: this.props.x,
      y: this.props.y,
      pitch: this.props.pitch,
      editMode: 0,
    }
    // console.log(this.state);
    // console.log("\n\n");
    /* Binds this to pressed() so it can change state when called */
  }

  editModePress(mode) {
    console.log("PIZZA IS THE BEST" + mode);
  }
  /**
   * Changing the color of the note that was pressed
   * red -> black OR black -> red
   */
  pressed() {
    if (this.state.color == 'black') {
      this.setState({ color: "red" });
    } else if (this.state.color == 'red') {
      this.setState({ color: "black" });
    }
  }
  /**
   * Changes the note when called. Simple stuff!
   * @param n must be within the NotesData.json
   * @param n == -1 then delete the note
   */
  ChangeNotePressed(n) {
    console.log("ChangeNotePressed");
  }
  ChangeColor(n) {
    this.setState({ color: "red" });
  }
  shouldComponentUpdate(nextProps) {
    console.log("WORKED\n");
    console.log(nextProps);
    this.state = nextProps;
  //   // console.log(nextProps);
  //   console.log(this.state);
  //   this.setState({});
  //   // console.log("ERGFAWFEAW\n");
  //   // console.log(nextProps);
  //     // if(JSON.stringify(this.props.user) !== JSON.stringify(nextProps.user)) // Check if it's a new user, you can also use some unique property, like the ID
  //     // {
  //     //        this.updateUser();
  //     // }
  }
  /**
   * Renders the note with its path
   */
  render() {
    console.log("state: ");
    console.log(this.state);
    // console.log("Rendering Notes\n");
    // console.log(this.props);
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    /* rendering the path of the note num */
    return (
      <G stroke="black" stroke-width="0" fill={this.state.color}>
        <Path x={[((this.state.x) * (betweenNotes)) + NoteSVG[this.state.note].adjustX].join(' ')} y={([((this.state.y) * (start)) + (this.props.pitch * SCREEN_HEIGHT / 164) + NoteSVG[this.state.note].adjustY].join(' '))} transform={['scale(', NoteSVG[this.state.note].scale1, NoteSVG[this.state.note].scale2, ')'].join(' ')} d={[NoteSVG[this.state.note].data].join(' ')} />
      </G>
    )
  }
};

// export default NotesObjects;
