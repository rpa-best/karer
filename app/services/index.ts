import { CRUDService, ReadOnlyService } from "./utils";


export class CarService extends CRUDService {
    constructor() {
        super('/onec/car/')
    }
}

export class DriverService extends CRUDService {
    constructor() {
        super('/onec/driver/')
    }
}

export class NomenclatureService extends ReadOnlyService {
    constructor() {
        super('/onec/nomenclature/')
    }
}

export class SenderService extends ReadOnlyService {
    constructor() {
        super('/onec/sender/')
    }
}

export class OrganizationService extends ReadOnlyService {
    constructor() {
        super('/onec/organization/')
    }
}

export class SpecificationService extends ReadOnlyService {
    constructor() {
        super('/onec/specification/')
    }
}

export class OrderService extends ReadOnlyService {
    constructor() {
        super('/order/')
    }
}
