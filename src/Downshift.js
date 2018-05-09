import React from 'react';
import Downshift from 'downshift';
import matchSorter from 'match-sorter';

const itemToString = item => (item ? item : '');

const DownshiftInput = ({ input, meta, placeholder, items, ...rest }) => (
  <Downshift
    {...input}
    onInputValueChange={inputValue => {
      input.onChange(inputValue)
    }}
    itemToString={itemToString}
    selectedItem={input.value}
  >
    {({
      getInputProps,
      getItemProps,
      getLabelProps,
      isOpen,
      inputValue,
      highlightedIndex,
      selectedItem
    }) => {
      const filteredItems = matchSorter(items, inputValue, {
        keys: ['value'],
        maxRanking: matchSorter.rankings.STARTS_WITH
      })
      return (
        <div className="downshift" style={{ position: 'relative' }}>
          <input
            {...getInputProps({
              name: input.name,
              placeholder
            })}
          />
          {isOpen &&
            !!filteredItems.length && (
              <div
                className="downshift-options"
                style={{
                  background: 'white',
                  position: 'absolute',
                  width: '27vw',
                  top: '100%',
                  left: 0,
                  right: 0,
                  zIndex: 4
                }}
              >
                {filteredItems.map(({ value, }, index) => (
                  <div
                    {...getItemProps({
                      key: value,
                      index,
                      item: value,
                      style: {
                        backgroundColor:
                          highlightedIndex === index ? 'lightgray' : 'white',
                        fontWeight: selectedItem === value ? 'bold' : 'normal',
                        width: '97.5%',
                        border: '0.05vw solid rgba(70,70,70,0.1)',
                        margin: '0 auto'
                      }
                    })}
                  >
                    {value}
                  </div>
                ))}
              </div>
            )}
        </div>
      )
    }}
  </Downshift>
)

export default DownshiftInput;