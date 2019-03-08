import React from 'react';
import { ListItem, Dimensions,TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import { Col, Row, Grid } from "react-native-easy-grid";
import Icon from 'react-native-vector-icons/AntDesign'
import PinchZoomView from 'react-native-pinch-zoom-view';


import { Svg } from 'expo';
const { Circle, Rect, Path, Line, Text, G, Defs, Use } = Svg;

// https://oblador.github.io/react-native-vector-icons/
// var sampleJson = require('./testRichard.json');
var sampleJson = require('./testRichard.json');
var NoteSVG = require('./NotesData.json');
var MiscJson = require('./EditMisc.json');
var NotesList = [];
// var ran1 = [0,5,10,15,20,25,30,35,40,45,50,55]

// var styles = require('../style');
const SCREEN_WIDTH = Dimensions.get('window').width
const SCREEN_HEIGHT = Dimensions.get('window').height
var colorr = "#00ffff";
var idCounter = 0;
var Section;
var totalBeats;
var screenSize = SCREEN_HEIGHT;


class NoteObjects extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      NoteNum: "EFF",
      color: "black",
    }
  }

  componentDidMount() {}

  pressed() {
    console.log("Pressed");
    if(this.state.color == "black"){
      this.setState({
        color: "red"
      })
    }else{
      this.setState({
        color: "black"
      })
    }
  }

  PRESSEDA() {
    console.log("HELLO");
  }

  // <TouchableOpacity
  //   style={styles.button}
  //   onPress={this.onPress}
  // >
  //   <Text> Touch Here </Text>
  // </TouchableOpacity>

  render(){
    console.log("RENDERING!!!!!!!!\n");
    console.log(this.props);
    let mesureLength = SCREEN_WIDTH/10;
    let start = SCREEN_HEIGHT/8;
    let betweenNotes = SCREEN_WIDTH/11;
    let x = (this.props._id%9)
    let y = Math.ceil(this.props._id/9);
    if(this.props._id == 0){
      y = 1;
    }else if(this.props._id%9 == 0){
      y++;
    }
    let pitch = this.props.pitch;
    if(pitch == 0)
     pitch++;
    x++;

    return (
      <G stroke="black" stroke-width="0" fill={this.state.color}>
        <Path x={[((x)*(SCREEN_WIDTH/11))+ NoteSVG[this.props.note].adjustX].join(' ')} y={([((y)*(SCREEN_HEIGHT/8))+ (this.props.pitch*SCREEN_HEIGHT/164) + NoteSVG[this.props.note].adjustY].join(' '))} transform={['scale(', NoteSVG[this.props.note].scale1, NoteSVG[this.props.note].scale2, ')'].join(' ')} d={[NoteSVG[this.props.note].data].join(' ')}/>
        <Rect
          x={[((x)*(SCREEN_WIDTH/11)) + mesureLength*NoteSVG[this.props.note].HitBoxX].join(' ')}
          y={[((y)*(SCREEN_HEIGHT/8)) + NoteSVG[this.props.note].HitBoxY + (NoteSVG[this.props.note].flipY*(pitch)*SCREEN_HEIGHT/110)].join(' ')}
          width={[NoteSVG[this.props.note].flipX * (mesureLength/1.1)].join(' ')}
          height={[NoteSVG[this.props.note].flipY * (-start/1.6)].join(' ')}
          fill="none"
          strokeWidth="1"
          onPress={() => this.PRESSEDA()}
        />
      </G>

    )
  }


   // onPress={() => this.pressed(this)}

  // render(){
  //   return (
  //     <G x="0" stroke="black" stroke-width="0" y="0" fill={[this.color].join(' ')}>
  //       {this.Notes()}
  //     </G>
  //   )
  // }
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

  componentDidMount() {}

  componentWillMount() {
    console.log("Component will mount!")
    NotesList = [];
    // for (let i = 0; i < sampleJson.notes.length; i++) {
    for (let i = 0; i < 2; i++) {
      NotesList.push(<NoteObjects _id={i} update={this.updateFunc} note={sampleJson.notes[i].note} len={sampleJson.notes[i].length} pitch={sampleJson.notes[i].pitch}/>);
    }
  }

  setTitle(title){
    let start = SCREEN_HEIGHT/8;
    return (
      <Svg height="100%" width="100%">
        <Text
            stroke="black"
            fontSize="20"
            x={[SCREEN_WIDTH/2].join(' ')}
            y={[start/2].join(' ')}
            textAnchor="middle"
        >{title}</Text>
      </Svg>
    )
  }

  placeVerticalLines(line){
    let mesureLength = SCREEN_WIDTH/10;
    let start = SCREEN_HEIGHT/8;
    start *= line
    return (
      <Svg height="100%" width="100%">
        {this.VerticalSection(mesureLength, start)}
        {this.VerticalSection(mesureLength*5.25, start)}
        {this.VerticalSection(mesureLength*9.05, start)}
      </Svg>
    )
  }

  pressHandler(Note){

    if (Note.color == "red" && Note.note != 0){
      Note.color = "black"
    }else if(Note.color == "black" && Note.note != 0){
      Note.color = "red"
    }
    this.setState({ state: this.state });
  }

  lineSection(){
    let amountOfMeasure = [];
    let spaceBetween = SCREEN_HEIGHT/82;
    let mesureLength = SCREEN_WIDTH/10;
    let start = SCREEN_HEIGHT/8;
    let betweenNotes = SCREEN_WIDTH/11;
    Section++;
    let x = 1;
    if(Section%2 == 0)
      x = 4.8;
    let y = Math.floor(Section/2);
    if(Section == 1){
      y = 0;
    }
    // console.log((((parseInt(Math.ceil((NotesList.length)/4.5/2))+1)*start + (5*SCREEN_HEIGHT/110)) + ":" + screenSize)
    if(((parseInt(Math.ceil((NotesList.length)/4.5/2))+1)*start + (5*SCREEN_HEIGHT/110)) > screenSize){
      screenSize += 500;
    }
    for (let i = 0; i < Math.ceil((NotesList.length)/4.5); i++) {
      amountOfMeasure.push(
        <Svg height="100%" width="100%">
          <Path x={[x*mesureLength].join(' ')} y={[((parseInt(i/2))+1)*start].join(' ')} transform={['scale(', .8, .4, ')'].join(' ')}  style="fill:green"
          d={[MiscJson[0].data].join(' ')}/>
          {this.placeVerticalLines(((parseInt(i/2))+1))}
        </Svg>
      )
    }
    return amountOfMeasure
  }

  VerticalSection(x, y){
    return (
      <Svg height="100%" width="100%">
        <Line
            x1={[x].join(' ')}
            y1={[y].join(' ')}
            x2={[x].join(' ')}
            y2={[y+(4*(SCREEN_HEIGHT/82))].join(' ')}
            stroke="black"
            strokeWidth="1"
        />
      </Svg>
    )
  }

  updateFunc(alert){
    console.log("GWFDigrjejgioperjgreaoyigjaw4og\n")
    // this.setState({
    //   alert: alert
    // })
  }

  setNotes(){
      let NotesL = [];
      for (let i = 0; i < NotesList.length; i++) {
        NotesL.push(<NoteObjects i = "Bob"/>);
      }
      return NotesL;
    }

  test(x){
    console.log("RENDERED");
    return (
      <G>
        <Rect
            x={x}
            y="0"
            width="10%"
            height="10%"
            fill="blue"
            strokeWidth="1"
            onPress={() => alert("Steven")}
          />
      </G>
    )
  }

  render(){
    console.log("First Render in note\n");
    // NotesList = [];
    // for (let i = 0; i < sampleJson.notes.length; i++) {
    //   NotesList.push(<NoteObjects _id={i} update={this.updateFunc} note={sampleJson.notes[i].note} len={sampleJson.notes[i].length} pitch={sampleJson.notes[i].pitch}/>);
    // }
    totalBeats = 0;
    backButton = require('../assets/back.png')
    let mesureLength = SCREEN_WIDTH/10;
    let start = SCREEN_HEIGHT/8;
    let betweenNotes = SCREEN_WIDTH/11;
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
          <Svg height={[screenSize].join(' ')}  width="100%">
            {this.test(0)}
            {this.test(50)}
          </Svg>
        </ScrollView>
      </View>
    )
  }
};

// <Svg height={[screenSize].join(' ')}  width="100%">
//   {this.setTitle("Steven is the Best")}
//   {this.lineSection()}
//   {this.lineSection()}
//   {NotesList}
// </Svg>

  function mapStateToProps(state) {}

  function mapDispatchToProps(dispatch) {}

//https://www.reduceimages.com/final_image.php?image=facde4b135
//30
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor:"white",
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
