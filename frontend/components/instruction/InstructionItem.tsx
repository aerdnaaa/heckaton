import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { Instruction } from './InstructionProps'

const InstructionItem = ({ instruction }: Instruction) => {
    return (
        <View style={styles.instructionItem}>
            <Text>{instruction}</Text>
        </View>
    )
}

export default InstructionItem

const styles = StyleSheet.create({
    instructionItem: {
        paddingTop: 10,
    }
})