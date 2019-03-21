/**
 * importing all the things I need to make this monster.
 * This includes but not limited to, React, react-native, react-redux,
 * react-native-easy-Grid, react-native-vector-icons/AntDesign
 * react-native-pinch-zoom-view, expo, and most importantly SVG.
 */

import React from 'react';
import { ListItem, Dimensions, TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import { Col, Row, Grid } from "react-native-easy-grid";
import Icon from 'react-native-vector-icons/AntDesign'
import PinchZoomView from 'react-native-pinch-zoom-view';


import { Svg } from 'expo';
const { Circle, Rect, Path, Line, Text, G, Defs, Use } = Svg;

/* Icon used from here for back button, this might be taken away */
// https://oblador.github.io/react-native-vector-icons/

// var sampleJson = require('./testRichard.json');
var sampleJson = require('./SampleMusicSheet.json');
var NoteSVG = require('./NotesData.json');
var MiscJson = require('./EditMisc.json');

var NotesList = [];

var NotesListByMeasure = [];
// var ran1 = [0,5,10,15,20,25,30,35,40,45,50,55]

// var styles = require('../style');

/* getting the dims of the screen that is accessing this code */
const SCREEN_WIDTH = Dimensions.get('window').width
const SCREEN_HEIGHT = Dimensions.get('window').height

/* this is the total amount of beats in the music sheet currently */
var totalBeats = 0;

/* Setting a varible for the screen_height that can be modified */
var screenSize = SCREEN_HEIGHT;
/* how far to make the screen go down */
var screenExtendSize = 0;

/*
 * This is the Component that holds all the notes and
 * renders each note depending on the note num, pitch, and length
 */
class NoteObjects extends React.Component {

  /**
   * This sets up the state and the functions to
   * change the state
   */
  constructor(props) {
    super(props);
    // console.log(NotesListByMeasure[props._id2][props._id1]);

    /* Settings up vairbles */

    let xLoc = props._id1;

    let yLoc = Math.floor(props._id2 / 2);
    if (props._id2 % 2 != 0) {
      xLoc += 5;
    }

    yLoc += 1;
    xLoc += 1;

    // xLoc++;
    /* Sets up the state with note num, pitch, Location, and color */
    this.state = {
      note: this.props.note,
      color: this.props.color,
      beatLength: this.props.len,
      x: xLoc,
      y: yLoc,
      pitch: this.props.pitch,
      measure: props._id2,
      measureNum: props._id1,
      editMode: 0,
    }
    // console.log(this.state);
    // console.log("\n\n");
    /* Binds this to pressed() so it can change state when called */
    this.pressed = this.pressed.bind(this);
    this.props.ChangeColor = this.pressed;
    this.ChangeNotePressed = this.ChangeNotePressed.bind(this);
    this.props.ChangeNote = this.ChangeNotePressed;
    this.editModePress = this.editModePress.bind(this);
    this.props.editMode = this.editModePress;
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
    if (n == -1) {
      NotesList.splice(this.props._id);
    } else {
      this.setState({ note: n });
    }
  }


  ChangeColor(n) {
    this.setState({ color: "red" });
  }

  // shouldComponentUpdate(nextProps) {
  //   console.log("WORKED\n");
  //   // console.log(nextProps);
  //   console.log(this.state);
  //   this.setState({});
  //   // console.log("ERGFAWFEAW\n");
  //   // console.log(nextProps);
  //     // if(JSON.stringify(this.props.user) !== JSON.stringify(nextProps.user)) // Check if it's a new user, you can also use some unique property, like the ID
  //     // {
  //     //        this.updateUser();
  //     // }
  // }

  /**
   * Renders the note with its path
   */
  render() {

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


class EditMusicScreen extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      NotesL: NotesList,
      colorProp: 'black',
      alert: false,
    };
  }

  static navigationOptions = {
    title: 'Welcome', header: null
  };

  componentDidMount() { }

  componentWillMount() {
    console.log("Component will mount!")
    let Extrarows = 0;
    screenExtendSize = 0;
    totalBeats = 0;
    NotesList = [];
    // for (let i = 0; i < sampleJson.notes.length; i++) {
    for (let i = 0; i < sampleJson.notes.length; i++) {
      Extrarows += sampleJson.notes[i].length
      totalBeats += sampleJson.notes[i].length;
      NotesList.push(<NoteObjects _id={i} note={sampleJson.notes[i].note} len={sampleJson.notes[i].length} pitch={sampleJson.notes[i].pitch} color="black" />);
    }

    screenExtendSize += ((Math.ceil(Extrarows / 8) - 7) * SCREEN_HEIGHT / 9);
    if (screenExtendSize < 0) {
      screenExtendSize = 0;
    }
  }

  setTitle(title) {
    let start = SCREEN_HEIGHT / 8;
    return (
      <Svg height="100%" width="100%">
        <Text
          stroke="black"
          fontSize="20"
          x={[SCREEN_WIDTH / 2].join(' ')}
          y={[start / 2].join(' ')}
          textAnchor="middle"
        >{title}</Text>
      </Svg>
    )
  }

  placeVerticalLines(line) {
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    start *= line
    return (
      <Svg height="100%" width="100%">
        {this.VerticalSection(mesureLength, start)}
        {this.VerticalSection(mesureLength * 5.25, start)}
        {this.VerticalSection(mesureLength * 9.05, start)}
      </Svg>
    )
  }

  pressHandler(Note) {

    if (Note.color == "red" && Note.note != 0) {
      Note.color = "black"
    } else if (Note.color == "black" && Note.note != 0) {
      Note.color = "red"
    }
    this.setState({ state: this.state });
  }

  lineSection() {
    // console.log(totalBeats);
    let Measures = [];
    let spaceBetween = SCREEN_HEIGHT / 82;
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    // let xyz = mesureLength/10.993;
    for (let i = 0; i < Math.ceil(totalBeats / 8); i++) {
      Measures.push(
        <G height="100%" width="100%" key={i}>
          <Path x={[mesureLength].join(' ')} y={[(i + 1) * start].join(' ')} transform={['scale(', mesureLength / 25, mesureLength / 107, ')'].join(' ')} style="fill:green"
            d={[MiscJson[0].data].join(' ')} />
          {this.VerticalSection(mesureLength, start * (i + 1))}
          {this.VerticalSection(mesureLength * 9, start * (i + 1))}
        </G>
      )
    }
    return Measures;
  }

  VerticalSection(x, y) {
    return (
      <G height="100%" width="100%">
        <Line
          x1={[x].join(' ')}
          y1={[y].join(' ')}
          x2={[x].join(' ')}
          y2={[y + (4 * (SCREEN_HEIGHT / 82))].join(' ')}
          stroke="black"
          strokeWidth="1"
        />
      </G>
    )
  }

  updateFunc(alert) {
    // console.log("GWFDigrjejgioperjgreaoyigjaw4og\n")
    // this.setState({
    //   alert: alert
    // })
  }

  /**
   * @deprecated Look at @renderMeasureBoxes for its replacement
   * Reason: We do not click on notes anymore you click on measures and
   * edit the measure instead of an note.
   */
  renderHitBoxes(i) {
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    let ret = [];
    for (let j = 0; j < NotesListByMeasure[i].length; j++) {
      totalBeats += NotesListByMeasure[i][j].props.len;
      let hitBoxSize = (-1) * Math.log10(.020 * (NotesListByMeasure[i].length))
      /* Settings up vairbles */
      let xLoc = NotesListByMeasure[i][j].props._id1;

      let yLoc = Math.floor(NotesListByMeasure[i][j].props._id2 / 2);
      if (NotesListByMeasure[i][j].props._id2 % 2 != 0) {
        xLoc += 5;
      }

      yLoc += 1;
      xLoc += 1;
      // console.log("HEREREREREW" + yLoc + " : " + xLoc + " Length: " + NotesListByMeasure[i].length + " HitBox: " +  hitBoxSize);

      let pitch = NotesListByMeasure[i][j].props.pitch;

      if (NotesListByMeasure[i][j].props.note != 0) {
        ret.push(
          <Rect
            x={[((xLoc) * (SCREEN_WIDTH / 11)) + mesureLength * NoteSVG[NotesListByMeasure[i][j].props.note].HitBoxX - SCREEN_WIDTH / 70].join(' ')}
            y={[((yLoc) * (SCREEN_HEIGHT / 8)) + NoteSVG[NotesListByMeasure[i][j].props.note].HitBoxY + (NoteSVG[NotesListByMeasure[i][j].props.note].flipY * (pitch) * SCREEN_HEIGHT / 110)].join(' ')}
            width={[NoteSVG[NotesListByMeasure[i][j].props.note].flipX * (mesureLength / 1.1) * hitBoxSize].join(' ')}
            height={[NoteSVG[NotesListByMeasure[i][j].props.note].flipY * (-start / 1.6)].join(' ')}
            onPress={() => this.onPressHitBox(i, j)}
            fill="blue"
            strokeWidth="0"
            fillOpacity="0"
          />
        )
      }

    }
    return ret;
  }

  renderMeasureBoxes(i, j) {
    let spaceBetween = SCREEN_HEIGHT / 82;
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    if (j == 0) {
      return (
        <Rect
          x={[mesureLength * 1].join(' ')}
          y={[start * (i + 1) - spaceBetween].join(' ')}
          width={[mesureLength * 4].join(' ')}
          height={[spaceBetween * 6].join(' ')}
          onPress={() => this.onPressHitBox(0, i)}
          fill="blue"
          strokeWidth="0"
          fillOpacity=".1"
        />
      )
    } else {
      return (
        <Rect
          x={[mesureLength * 5].join(' ')}
          y={[start * (i + 1) - spaceBetween].join(' ')}
          width={[mesureLength * 4].join(' ')}
          height={[spaceBetween * 6].join(' ')}
          onPress={() => this.onPressHitBox(1, i)}
          fill="yellow"
          strokeWidth="0"
          fillOpacity=".1"
        />
      )
    }
  }

  onPressHitBox(x, y) {
    console.log("x: " + x + " y: " + y);
    // console.log(NotesListByMeasure[(y*2) + x])

    //Send to measure Screen
    this.props.navigation.navigate('ViewMeasure', { arr: NotesListByMeasure[(y * 2) + x] });
  }

  initNotesListByMeasure() {
    let beatsPerMeasure = 0;
    let measureNotes = [];
    let xCord = 0;
    for (let i = 0; i < sampleJson.notes.length; i++) {
      // console.log("X");
      if (((beatsPerMeasure + sampleJson.notes[i].length) > 4) || (NoteSVG[sampleJson.notes[i].note].title == "clef")) {
        // console.log("XXXXXXX");
        NotesListByMeasure.push(measureNotes);
        measureNotes = [];
        beatsPerMeasure = 0;
      }
      if (measureNotes.length == 0) {
        xCord = 0;
      }
      if (NoteSVG[sampleJson.notes[i].note].title == "clef") {
        xCord = 0;
      }

      measureNotes.push(<NoteObjects key={i} _id1={xCord} _id2={NotesListByMeasure.length - 1} note={sampleJson.notes[i].note} len={sampleJson.notes[i].length} pitch={sampleJson.notes[i].pitch} color="black" />);
      beatsPerMeasure += sampleJson.notes[i].length;
      if (NoteSVG[sampleJson.notes[i].note].title == "clef") {
        xCord = 1;
      }

      xCord += sampleJson.notes[i].length;
    }
    if (measureNotes.length != 0) {
      NotesListByMeasure.push(measureNotes);
    }
    NotesListByMeasure.splice(0, 1);
    for (let i = 0; i < NotesListByMeasure.length; i++) {
      for (let j = 0; j < NotesListByMeasure[i].length; j++) {
        console.log(NotesListByMeasure[i][j].props.note);
      }
      console.log("\n");
    }
  }

  displayNotes() {
    let ret = [];
    /* Two loops because we want the boxes to be rendered OVER the notes */
    for (var i = 0; i < NotesListByMeasure.length; i++) {
      ret.push(NotesListByMeasure[i])
      // ret.push(this.renderHitBoxes(i));
    }
    for (var i = 0; i < (NotesListByMeasure.length / 2); i++) {
      // ret.push(this.renderMeasureBoxes(i,0))
      // ret.push(this.renderMeasureBoxes(i,1))
    }
    return ret;
  }

  render() {
    console.log("First Render in note\n");
    NotesListByMeasure = [];
    // screenExtendSize = 0;
    this.initNotesListByMeasure();
    // console.log(NotesListByMeasure.props.note);
    // totalBeats = 0;
    backButton = require('../assets/back.png')
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    Section = 0;

    return (
      <View style={styles.container}>
        <Header
          statusBarProps={{ barStyle: 'light-content' }}
          barStyle="light-content" // or directly
          leftComponent={
            <Button
              onPress={() => this.props.navigation.navigate('ViewCompScreen')}
              icon={
                <Icon
                  name="left"
                  size={15}
                  color="white"
                />
              }
              type="clear"
            />
          }
          centerComponent={{ text: 'Rhythm', style: { color: '#fff' } }}
          containerStyle={{
            backgroundColor: 'black',
            justifyContent: 'space-around',
          }}
        />
        <ScrollView>
          <Svg height={[screenSize + screenExtendSize].join(' ')} width="100%">
            {this.setTitle("Music Sheet_1")}

            {this.displayNotes()}
            {this.lineSection()}
          </Svg>

        </ScrollView>
      </View>
    )
  }
};

function mapStateToProps(state) {
  return {}
}

function mapDispatchToProps(dispatch) {
  return {}
}

//https://www.reduceimages.com/final_image.php?image=facde4b135
//30
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
  },
  header: {
    flex: .13,
    backgroundColor: 'black',
  },
  button: {
    alignItems: 'center',
    top: '90%',
    right: '40%',
  },
  background: {
    resizeMode: 'cover',
  },
  list: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: 'pink',
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(EditMusicScreen);
