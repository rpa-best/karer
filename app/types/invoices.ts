import type { Car } from "./car"
import type { Driver } from "./driver"
import type { Nomenclature } from "./onec"

export interface InvoiceNomenclature {
    created_at: string
    nomenclature: string | null
    value: number
    invoice: number | undefined
}

export interface Invoice {
    id: number
    number: string
    created_at: string
    updated_at: string
    status: string
    address: string
    type: string
    comment: string
    org: string
    specification: string
    nomenclatures: InvoiceNomenclature[]
}

export interface DriverComment {
    id: number
    status: 'loading' | 'ok' | 'error'
    text: string
    created_at: string
}

export interface Order {
    uuid: string
    car: Car
    driver: Driver
    nomenclature: Nomenclature
    invoice: Invoice
    address: string
    per_price: number
    additive: number
    order: number
    fact: number
    done: boolean
    comment: string
    created_at: string
    updated_at: string
}

export interface OrderForm {
    uuid: string
    car: number
    driver: number
    nomenclature: string
    invoice: number
    address: string
    per_price: number
    additive: number
    order: number
    fact: number
    comment: string
}
