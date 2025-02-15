import { StyleSheet, Text, View, ScrollView } from 'react-native';
import React from 'react';
import { InstructionListProps } from './InstructionProps';
import { CiCircleList } from "react-icons/ci";
import InstructionItem from './InstructionItem';

const InstructionComponent = ({ instructions }: InstructionListProps) => {
    if (!instructions?.length) {
        return;
    }
    return (
        <View style={styles.instructionContainer}>
            <Text style={styles.mediumFont}><CiCircleList style={styles.icon} />Instructions</Text>
            <ScrollView>
                {instructions.map((instruction) => {
                    return <InstructionItem instruction={instruction} />
                })}

            </ScrollView>
        </View>
    )
}

export default InstructionComponent

const styles = StyleSheet.create({
    icon: {
        paddingRight: 5,
    },
    mediumFont: {
        fontSize: 20,
        fontWeight: 'bold',
        display: 'flex',
        alignItems: 'center'
    },

    instructionContainer: {
        width: '48%',
    }
})