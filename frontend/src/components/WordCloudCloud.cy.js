import React from 'react'
import Cloud from './WordCloud'

describe('<Cloud />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<Cloud />)
  })
})