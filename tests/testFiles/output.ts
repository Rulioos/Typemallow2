export enum MyAutoEnum {
	enum1, 
	enum2, 
}

export enum MyNonAutoEnum {
	enum1 = 100,
	enum2 = 200,
	enum3 = "Baguette",
}

export interface Boo {
	some_field: string;
	my_enum_field: MyAutoEnum;
}

export interface Foo {
	some_field: string;
	another_field: string;
	my_field: boolean;
	my_interface_field: Boo;
}

