export enum MyAutoEnum {
	enum1,
	enum2,
}

export enum MyNonAutoEnum {
	enum1,
	enum2,
	enum3,
}

export enum MyNonAutoEnumWhereValuesAreNotImportant {
	enum1,
	enum2,
	enum3,
}

export enum MyAutoEnumButValuesMatter {
	enum1 = 1,
	enum2 = 2,
}

export interface Bar {
	some_field: string;
	my_enum_field: MyAutoEnum;
}

export interface Foo {
	some_field: string;
	another_field: string;
	my_field: boolean;
	my_interface_field: Bar;
	my_interfaces_fields: Bar[];
}

