/* tslint:disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL fragment: AddressFragment
// ====================================================

export interface AddressFragment_country {
  __typename: "CountryDisplay";
  code: string;
  country: string;
}

export interface AddressFragment {
  __typename: "Address";
  id: string;
  city: string;
  cityArea: string;
  companyName: string;
  country: AddressFragment_country | null;
  countryArea: string;
  firstName: string;
  lastName: string;
  phone: string | null;
  postalCode: string;
  streetAddress1: string;
  streetAddress2: string;
}
